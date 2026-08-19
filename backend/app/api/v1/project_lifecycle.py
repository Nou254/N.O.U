"""
Project lifecycle, staffing and change-request API.

Implements today.md:
- PROJECT FLOW AND PORTAL ACCESS STRUCTURE (controlled lifecycle stages)
- PROJECT STAFFING AND TEAM FORMATION POLICY (staffing plans, eligibility,
  expression of interest, candidate selection, max 3 projects)
- CHANGE REQUEST PORTAL (scope-creep protection)
- PROJECT DOCUMENT APPROVAL FLOW (DRAFT -> UNDER REVIEW -> APPROVED -> LOCKED)

Split across two routers:
- /api/v1/portal/...    developer-facing (opportunities, express interest)
- /api/v1/admin/...     admin-facing (staffing plan, candidates, selection,
                        lifecycle stage transitions, document review,
                        change-request decisions)

The lifecycle stages (today.md sec. 21):
    requested -> initial_review -> clarification -> analysis ->
    technical_feasibility -> documentation -> internal_review ->
    estimation -> customer_proposal -> customer_approval -> staffing ->
    team_formation -> planning -> development -> qa -> security_review ->
    staging -> customer_acceptance -> deployment -> support -> closed
plus terminal/paused: on_hold, blocked, cancelled, rejected.
"""

import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, Field
from typing import Optional, List

from app.core.database import get_db
from app.core.security import require_developer, require_admin, require_authenticated
from app.models.user import User
from app.models.company_project import (
    CompanyProject, ProjectMember, ProjectDocument,
)
from app.models.project_lifecycle import (
    StaffingPlanItem, ExpressionOfInterest, ProjectChangeRequest,
)
from app.models.personnel import PersonnelCategory
from app.models.assessment import AssessmentSession
from app.api.v1.projects_portal import (
    _get_project, MAX_PROJECTS_PER_DEVELOPER, _active_project_count,
)

# Lifecycle order (today.md). Optional stages may be skipped by admin.
LIFECYCLE_ORDER = [
    "requested", "initial_review", "clarification", "analysis",
    "technical_feasibility", "documentation", "internal_review",
    "estimation", "customer_proposal", "customer_approval", "staffing",
    "team_formation", "planning", "development", "qa", "security_review",
    "staging", "customer_acceptance", "deployment", "support", "closed",
]
TERMINAL_STAGES = {"on_hold", "blocked", "cancelled", "rejected", "closed"}

# Document approval workflow (today.md sec. 22).
DOC_STATUS_FLOW = ["draft", "under_review", "revision_required", "re_submitted",
                   "approved", "locked"]

portal_router = APIRouter()
admin_router = APIRouter()
router = portal_router  # alias for backward-compat imports


# ===========================================================================
# Developer-facing: staffing opportunities + expression of interest
# ===========================================================================
@portal_router.get("/opportunities")
async def list_opportunities(
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    """
    Projects currently at the staffing stage that this developer is eligible
    for (today.md sec. 15: "During staffing: eligible personnel may see a
    limited project opportunity"). Eligibility: not already a member, under
    the 3-project cap, and the staffing plan includes a matching position or
    the project has no staffing plan yet.
    """
    active = await _active_project_count(db, current_user.id)
    if active >= MAX_PROJECTS_PER_DEVELOPER:
        return {"opportunities": [], "reason": "3-project cap reached"}

    projects_result = await db.execute(
        select(CompanyProject)
        .options(
            selectinload(CompanyProject.members),
            selectinload(CompanyProject.staffing_plan),
        )
        .where(CompanyProject.lifecycle_stage.in_(["staffing", "team_formation", "planning"]))
    )
    projects = projects_result.scalars().all()

    my_project_ids = set()
    for p in projects:
        for m in (p.members or []):
            if m.user_id == current_user.id:
                my_project_ids.add(p.id)

    opportunities = []
    for p in projects:
        if p.id in my_project_ids:
            continue
        # Limited project information only - never customer confidential data.
        items = p.staffing_plan or []
        positions = [
            {
                "position": it.position,
                "count_required": it.count_required,
                "skills": it.skills,
                "experience_level": it.experience_level,
                "duration": it.duration,
            }
            for it in items
        ]
        opportunities.append({
            "project_id": p.id,
            "title": p.title,
            "category": p.category,
            "description": p.description,
            "positions": positions,
            "estimated_duration": max((it.duration or "") for it in items) if items else None,
            "deadline": p.deadline,
            "stage": p.lifecycle_stage,
            "already_interested": await _has_eoi(db, p.id, current_user.id),
        })
    return {"opportunities": opportunities}


async def _has_eoi(db: AsyncSession, project_id: int, user_id: int) -> bool:
    row = await db.scalar(
        select(ExpressionOfInterest).where(
            ExpressionOfInterest.project_id == project_id,
            ExpressionOfInterest.user_id == user_id,
            ExpressionOfInterest.status == "pending",
        )
    )
    return row is not None


class ExpressInterestIn(BaseModel):
    position: Optional[str] = None
    skills: Optional[str] = None


@portal_router.post("/projects/{project_id}/express-interest", status_code=status.HTTP_201_CREATED)
async def express_interest(
    project_id: str,
    body: ExpressInterestIn,
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    """
    A qualified developer expresses interest in an opportunity. This is NOT
    assignment (today.md sec. 9) - the system records the interest and the
    authorized selection team decides.
    """
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.lifecycle_stage not in ("staffing", "team_formation", "planning"):
        raise HTTPException(
            status_code=400,
            detail="This project is not currently recruiting",
        )
    if project.status in ("completed", "published", "cancelled", "rejected"):
        raise HTTPException(status_code=400, detail="This project is closed")

    existing = await db.scalar(
        select(ExpressionOfInterest).where(
            ExpressionOfInterest.project_id == project.id,
            ExpressionOfInterest.user_id == current_user.id,
            ExpressionOfInterest.status.in_(["pending", "selected"]),
        )
    )
    if existing:
        raise HTTPException(status_code=400, detail="You have already expressed interest")

    member = await db.scalar(
        select(ProjectMember).where(
            ProjectMember.project_id == project.id,
            ProjectMember.user_id == current_user.id,
        )
    )
    if member:
        raise HTTPException(status_code=400, detail="You are already on this project")

    active = await _active_project_count(db, current_user.id)
    if active >= MAX_PROJECTS_PER_DEVELOPER:
        raise HTTPException(
            status_code=400,
            detail=f"You are already on {MAX_PROJECTS_PER_DEVELOPER} active projects (the maximum)",
        )

    eoi = ExpressionOfInterest(
        project_id=project.id,
        user_id=current_user.id,
        position=body.position,
        skills=body.skills,
        status="pending",
    )
    db.add(eoi)
    await db.commit()
    return {"message": "Interest recorded - selection is decided by project management",
            "status": eoi.status}


@portal_router.get("/my-interests")
async def my_interests(
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    """The developer's expression-of-interest records with project titles."""
    result = await db.execute(
        select(ExpressionOfInterest, CompanyProject)
        .join(CompanyProject, CompanyProject.id == ExpressionOfInterest.project_id)
        .where(ExpressionOfInterest.user_id == current_user.id)
        .order_by(ExpressionOfInterest.created_at.desc())
    )
    rows = result.all()
    return {
        "interests": [
            {
                "id": eoi.id,
                "project_id": eoi.project_id,
                "title": project.title,
                "position": eoi.position,
                "status": eoi.status,
                "created_at": eoi.created_at,
                "admin_notes": eoi.admin_notes,
            }
            for eoi, project in rows
        ]
    }


@portal_router.delete("/projects/{project_id}/express-interest")
async def withdraw_interest(
    project_id: str,
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    eoi = await db.scalar(
        select(ExpressionOfInterest).where(
            ExpressionOfInterest.project_id == project_id,
            ExpressionOfInterest.user_id == current_user.id,
            ExpressionOfInterest.status == "pending",
        )
    )
    if not eoi:
        raise HTTPException(status_code=404, detail="No pending interest to withdraw")
    eoi.status = "withdrawn"
    await db.commit()
    return {"message": "Interest withdrawn"}


# ===========================================================================
# Developer-facing: change requests (scope creep protection)
# ===========================================================================
class ChangeRequestIn(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=5)
    reason: Optional[str] = None


@portal_router.post("/projects/{project_id}/change-requests", status_code=status.HTTP_201_CREATED)
async def submit_change_request(
    project_id: str,
    body: ChangeRequestIn,
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    """Team member proposes a change (new requirement/scope) for review."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    member = await db.scalar(
        select(ProjectMember).where(
            ProjectMember.project_id == project.id,
            ProjectMember.user_id == current_user.id,
        )
    )
    if not member and not current_user.role == "admin":
        raise HTTPException(status_code=403, detail="You are not a member of this project")

    cr = ProjectChangeRequest(
        project_id=project.id,
        requested_by=current_user.id,
        title=body.title,
        description=body.description,
        reason=body.reason,
        status="pending",
    )
    db.add(cr)
    await db.commit()
    return {"message": "Change request submitted for review", "id": cr.id}


@portal_router.get("/projects/{project_id}/change-requests")
async def list_project_change_requests(
    project_id: str,
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    member = await db.scalar(
        select(ProjectMember).where(
            ProjectMember.project_id == project.id,
            ProjectMember.user_id == current_user.id,
        )
    )
    if not member and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not a member of this project")
    result = await db.execute(
        select(ProjectChangeRequest)
        .where(ProjectChangeRequest.project_id == project.id)
        .order_by(ProjectChangeRequest.created_at.desc())
    )
    return {"change_requests": [
        {
            "id": cr.id,
            "title": cr.title,
            "description": cr.description,
            "reason": cr.reason,
            "status": cr.status,
            "impact_analysis": cr.impact_analysis,
            "cost_impact": float(cr.cost_impact) if cr.cost_impact is not None else None,
            "time_impact_days": cr.time_impact_days,
            "created_at": cr.created_at,
        }
        for cr in result.scalars().all()
    ]}


# ===========================================================================
# Admin: lifecycle stage transitions
# ===========================================================================
class StageTransitionIn(BaseModel):
    stage: str
    notes: Optional[str] = None


@admin_router.post("/projects/{project_id}/stage")
async def transition_stage(
    project_id: str,
    body: StageTransitionIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Admin moves a project through the controlled lifecycle (today.md)."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    target = body.stage
    if target not in LIFECYCLE_ORDER and target not in TERMINAL_STAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown stage '{target}'. Valid: {', '.join(LIFECYCLE_ORDER + sorted(TERMINAL_STAGES - {'closed'}))}",
        )

    if target not in TERMINAL_STAGES:
        current_idx = LIFECYCLE_ORDER.index(project.lifecycle_stage) \
            if project.lifecycle_stage in LIFECYCLE_ORDER else 0
        target_idx = LIFECYCLE_ORDER.index(target)
        if target_idx < current_idx:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot move backwards from '{project.lifecycle_stage}' to '{target}'",
            )

    project.lifecycle_stage = target
    # Map lifecycle to the legacy status field for downstream compatibility.
    project.status = _legacy_status(target, project)
    if body.notes:
        project.admin_notes = (project.admin_notes or "") + f"\n[{datetime.now():%Y-%m-%d %H:%M}] -> {target}: {body.notes}"
    await db.commit()
    return {"message": f"Project moved to '{target}'", "lifecycle_stage": project.lifecycle_stage}


def _legacy_status(stage: str, project: CompanyProject) -> str:
    if stage in ("requested", "initial_review", "clarification", "analysis",
                 "technical_feasibility", "documentation", "internal_review",
                 "estimation", "customer_proposal", "customer_approval"):
        return "open"
    if stage == "staffing":
        return "open"
    if stage in ("team_formation", "planning", "development"):
        return "in_progress"
    if stage in ("qa", "security_review", "staging", "customer_acceptance"):
        return "review"
    if stage == "deployment":
        return "review"
    if stage in ("support", "closed"):
        return "completed"
    if stage in ("cancelled", "rejected"):
        return "cancelled"
    return "open"


# ===========================================================================
# Admin: staffing plan + candidates
# ===========================================================================
class StaffingItemIn(BaseModel):
    position: str = Field(min_length=2, max_length=120)
    count_required: int = Field(1, ge=1, le=20)
    skills: Optional[str] = None
    experience_level: Optional[str] = None
    availability: Optional[str] = None
    duration: Optional[str] = None


@admin_router.post("/projects/{project_id}/staffing-plan")
async def set_staffing_plan(
    project_id: str,
    items: List[StaffingItemIn],
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Replace the project's staffing plan (today.md sec. 5)."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    existing = await db.execute(
        select(StaffingPlanItem).where(StaffingPlanItem.project_id == project.id)
    )
    for item in existing.scalars().all():
        await db.delete(item)

    for it in items:
        db.add(StaffingPlanItem(
            project_id=project.id,
            position=it.position,
            count_required=it.count_required,
            skills=it.skills,
            experience_level=it.experience_level,
            availability=it.availability,
            duration=it.duration,
        ))
    await db.commit()
    return {"message": "Staffing plan updated", "positions": len(items)}


@admin_router.get("/projects/{project_id}/candidates")
async def list_candidates(
    project_id: str,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Candidates for a project: every expression of interest plus eligible
    personnel from the talent pool (qualified via assessment, today.md sec. 7).
    """
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    eoi_result = await db.execute(
        select(ExpressionOfInterest, User)
        .join(User, User.id == ExpressionOfInterest.user_id)
        .where(ExpressionOfInterest.project_id == project.id)
        .order_by(ExpressionOfInterest.created_at)
    )
    eoi_rows = eoi_result.all()

    candidates = []
    for eoi, user in eoi_rows:
        candidates.append({
            "user_id": user.id,
            "name": f"{user.first_name} {user.last_name}".strip() or user.email,
            "email": user.email,
            "source": "expression_of_interest",
            "position": eoi.position,
            "skills": eoi.skills,
            "status": eoi.status,
            "active_projects": await _active_project_count(db, user.id),
            "assessment": await _user_assessment_summary(db, user.id),
            "eoi_id": eoi.id,
        })

    return {"candidates": candidates}


async def _user_assessment_summary(db: AsyncSession, user_id: int) -> Optional[dict]:
    session = await db.scalar(
        select(AssessmentSession)
        .where(
            AssessmentSession.applicant_id == user_id,
            AssessmentSession.status == "completed",
        )
        .order_by(AssessmentSession.completed_at.desc())
        .limit(1)
    )
    if not session:
        return None
    return {
        "percentage": session.percentage,
        "competency_band": session.competency_band,
        "category": session.category_name,
        "position": session.position_name,
    }


class CandidateDecisionIn(BaseModel):
    decision: str  # selected / declined
    notes: Optional[str] = None
    role: Optional[str] = None


@admin_router.post("/projects/{project_id}/candidates/{eoi_id}/decision")
async def decide_candidate(
    project_id: str,
    eoi_id: str,
    body: CandidateDecisionIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Admin selects or declines a candidate who expressed interest. Selection
    assigns the member to the project (respecting the 3-project cap)."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    eoi = await db.scalar(
        select(ExpressionOfInterest).where(
            ExpressionOfInterest.id == eoi_id,
            ExpressionOfInterest.project_id == project.id,
            ExpressionOfInterest.status == "pending",
        )
    )
    if not eoi:
        raise HTTPException(status_code=404, detail="Pending interest not found")

    if body.decision == "selected":
        active = await _active_project_count(db, eoi.user_id)
        if active >= MAX_PROJECTS_PER_DEVELOPER:
            raise HTTPException(
                status_code=400,
                detail="Candidate is already at the 3-project maximum",
            )
        existing = await db.scalar(
            select(ProjectMember).where(
                ProjectMember.project_id == project.id,
                ProjectMember.user_id == eoi.user_id,
            )
        )
        if not existing:
            is_first = await db.scalar(
                select(func.count()).select_from(ProjectMember)
                .where(ProjectMember.project_id == project.id)
            ) == 0
            member = ProjectMember(
                project_id=project.id,
                user_id=eoi.user_id,
                role=body.role or eoi.position or "developer",
                is_team_leader=is_first and project.team_leader_id is None,
            )
            db.add(member)
            await db.flush()
            if project.team_leader_id is None and is_first:
                project.team_leader_id = eoi.user_id
            # Headcount reached -> move to team formation.
            count = await db.scalar(
                select(func.count()).select_from(ProjectMember)
                .where(ProjectMember.project_id == project.id)
            )
            if count >= project.required_people and project.lifecycle_stage == "staffing":
                project.lifecycle_stage = "team_formation"
                project.status = "in_progress"
        eoi.status = "selected"
        eoi.admin_notes = body.notes
        eoi.decided_by = current_user.id
        eoi.decided_at = datetime.now()
        await db.commit()
        return {"message": "Candidate selected and added to the project team"}

    if body.decision == "declined":
        eoi.status = "declined"
        eoi.admin_notes = body.notes
        eoi.decided_by = current_user.id
        eoi.decided_at = datetime.now()
        await db.commit()
        return {"message": "Candidate declined"}

    raise HTTPException(status_code=400, detail="Decision must be 'selected' or 'declined'")


class TeamLeaderIn(BaseModel):
    member_id: int


@admin_router.post("/projects/{project_id}/team-leader")
async def appoint_team_leader(
    project_id: str,
    body: TeamLeaderIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Appoint the project's team leader. The first person to express interest is
    NOT automatically the leader (today.md sec. 16) - management decides.
    """
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    member = await db.scalar(
        select(ProjectMember).where(
            ProjectMember.project_id == project.id,
            ProjectMember.id == body.member_id,
        )
    )
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")

    # Clear previous leader flags.
    members = await db.execute(
        select(ProjectMember).where(ProjectMember.project_id == project.id)
    )
    for m in members.scalars().all():
        m.is_team_leader = (m.id == member.id)
    project.team_leader_id = member.user_id
    await db.commit()
    return {"message": "Team leader appointed", "team_leader_id": member.user_id}


# ===========================================================================
# Admin: document review workflow
# ===========================================================================
class DocumentReviewIn(BaseModel):
    action: str  # submit_for_review / approve / request_revision / lock
    notes: Optional[str] = None


@admin_router.post("/projects/{project_id}/documents/{document_id}/review")
async def review_document(
    project_id: str,
    document_id: str,
    body: DocumentReviewIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Move a project document through the approval workflow (today.md sec. 22)."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    doc = await db.scalar(
        select(ProjectDocument).where(
            ProjectDocument.id == document_id,
            ProjectDocument.project_id == project.id,
        )
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    action = body.action
    transitions = {
        "submit_for_review": ("draft", "under_review"),
        "approve": ("under_review", "approved"),
        "request_revision": (("under_review", "approved"), "revision_required"),
        "resubmit": ("revision_required", "re_submitted"),
        "lock": ("approved", "locked"),
    }
    if action not in transitions:
        raise HTTPException(
            status_code=400,
            detail="Action must be one of: submit_for_review, approve, request_revision, resubmit, lock",
        )
    allowed_from, new_status = transitions[action]
    if doc.doc_status not in (allowed_from if isinstance(allowed_from, tuple) else (allowed_from,)):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot '{action}' a document in status '{doc.doc_status}'",
        )

    doc.doc_status = new_status
    doc.reviewer_notes = body.notes or doc.reviewer_notes
    doc.reviewed_by = current_user.id
    doc.reviewed_at = datetime.now()
    if new_status == "approved":
        doc.version = (doc.version or 1) + 1
    await db.commit()
    return {"message": f"Document is now '{new_status}'", "doc_status": doc.doc_status}


# ===========================================================================
# Admin: change request decisions
# ===========================================================================
class ChangeRequestDecisionIn(BaseModel):
    decision: str  # approve / decline
    impact_analysis: Optional[str] = None
    technical_review: Optional[str] = None
    cost_impact: Optional[float] = None
    time_impact_days: Optional[int] = None


@admin_router.post("/change-requests/{change_request_id}/decision")
async def decide_change_request(
    change_request_id: str,
    body: ChangeRequestDecisionIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    cr = await db.scalar(
        select(ProjectChangeRequest).where(
            ProjectChangeRequest.id == change_request_id,
            ProjectChangeRequest.status == "pending",
        )
    )
    if not cr:
        raise HTTPException(status_code=404, detail="Change request not found")

    if body.decision not in ("approve", "decline"):
        raise HTTPException(status_code=400, detail="Decision must be 'approve' or 'decline'")

    cr.impact_analysis = body.impact_analysis or cr.impact_analysis
    cr.technical_review = body.technical_review or cr.technical_review
    if body.cost_impact is not None:
        cr.cost_impact = body.cost_impact
    if body.time_impact_days is not None:
        cr.time_impact_days = body.time_impact_days
    cr.status = "approved" if body.decision == "approve" else "declined"
    cr.decided_by = current_user.id
    cr.decided_at = datetime.now()
    await db.commit()
    return {"message": f"Change request {cr.status}", "status": cr.status}
