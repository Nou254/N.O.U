"""
Company projects portal API.

Rules implemented:
- Admin posts projects/jobs (PDF/DOCX documentation) with a required headcount.
- Developers join projects: if required_people == 1 the first joiner works
  alone; if more are needed, project documentation is released only once the
  required number of developers have joined.
- A developer may work on at most 3 projects at a time.
- Overwhelmed teams may request up to 3 extra developers (who themselves are
  below the 3-project cap); an admin approves.
- Teams have a team leader; members take roles (e.g. database engineer) and
  are not restricted to one role.
- Members can chat; the AI (Groq via the key pool) can be called for help.
- The team leader submits a weekly progress report; the admin grades it (the
  admin's grade is the official percentage investors see).
- Every project must be completed and uploaded before its scheduled deadline;
  if that is not possible the team leader requests an extension (max 4 weeks).
- Finished projects are uploaded for admin review and can be published for
  customers under a gallery section (Games, Bots, Education, ...).
- Documents/help files are downloadable via short-lived signed URLs.
- Investors can VIEW project progress (read-only). Investors who are also
  developers have full member access.
"""

import base64
import hashlib
import hmac
import os
import time
import uuid
from datetime import datetime, date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status, Query, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.core.database import get_db
from app.core.rate_limit import check_rate_limit
from app.core.security import (
    require_admin, require_developer, get_current_user, require_role,
    require_authenticated,
)
from app.core.config import settings
from app.models.user import User
from app.models.company_project import (
    CompanyProject, ProjectMember, ProjectDocument, ProjectChatMessage,
    ExtraDeveloperRequest,
)
from app.models.project_release import ProjectRelease
from app.models.project_lifecycle import (
    StaffingPlanItem, ProjectChangeRequest,
)
from app.models.project_progress import (
    ProjectProgressReport, ProjectHelpRequest, ProjectDeadlineExtension,
)

router = APIRouter()

# A developer may hold at most 3 projects at a time.
MAX_PROJECTS_PER_DEVELOPER = 3
# Teams may request at most 3 extra developers.
MAX_EXTRA_DEVELOPERS = 3
# Deadline extensions may add at most 4 weeks (28 days) past the schedule.
MAX_EXTENSION_DAYS = 28
# Gallery sections when publishing completed projects for customers. The list
# follows the N.O.U. software-category classification (see today.md).
PUBLISH_SECTIONS = [
    "Games and Entertainment", "Bots", "Education and Learning",
    "Business and Enterprise", "Productivity and Personal Organization",
    "Finance and Accounting", "Health and Wellness",
    "Communication and Social Platforms", "E-Commerce and Retail",
    "Hospitality and Tourism", "Government and Public Administration",
    "Agriculture", "Transport and Logistics", "Security and Monitoring",
    "Networking and Infrastructure", "Developer and IT Tools",
    "Artificial Intelligence", "Multimedia and Creative Software",
    "Lifestyle and Personal Applications", "Religious and Community Systems",
    "Specialized and Custom Software", "Custom Development Services", "Other",
]
# Signed download URLs expire after this many seconds (short-lived so a
# copied link cannot be shared forever).
SIGNED_URL_TTL_SECONDS = 1800

# ---------------------------------------------------------------------------
# Short-lived signed download URLs (HMAC, SECRET_KEY-bound)
# ---------------------------------------------------------------------------
def _sign_scope(scope: str) -> str:
    """Create an expiring signed token for a resource scope.

    Format: <urlsafe(base64(scope))>.<expiry_unix>.<sha256_hmac>
    ``scope`` encodes the resource + the recipient class, e.g.
    ``doc:12:34:member`` (document 34 of project 12 for members).
    """
    expiry = int(time.time()) + SIGNED_URL_TTL_SECONDS
    payload = base64.urlsafe_b64encode(scope.encode()).decode().rstrip("=")
    message = f"{payload}:{expiry}".encode()
    signature = hmac.new(settings.SECRET_KEY.encode(), message, hashlib.sha256).hexdigest()
    return f"{payload}.{expiry}.{signature}"


def _resource_from_token(token: str) -> Optional[str]:
    """Return the decoded resource scope if the token is authentic + unexpired."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload, expiry, signature = parts
        if int(expiry) < time.time():
            return None
        message = f"{payload}:{expiry}".encode()
        expected = hmac.new(settings.SECRET_KEY.encode(), message, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            return None
        return base64.urlsafe_b64decode(payload.encode() + b"==").decode()
    except Exception:  # noqa: BLE001 - malformed token
        return None


# Optional auth: signed-URL downloads work without a Bearer header.
_optional_bearer = HTTPBearer(auto_error=False)


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_optional_bearer),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """Authenticated user or None (no exception when the header is absent)."""
    if not credentials:
        return None
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None
# Allowed software-release extensions (binaries are validated by extension
# because browsers send inconsistent MIME types for .apk/.exe/.zip etc.).
ALLOWED_RELEASE_EXTENSIONS = set(settings.ALLOWED_RELEASE_EXTENSIONS)

# Allowed document upload types (PDF / DOCX / text / images).
ALLOWED_DOC_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "image/jpeg",
    "image/png",
    "image/webp",
}

require_member_or_investor = require_role(["developer", "investor", "admin"])


def _member_count(project: CompanyProject) -> int:
    return len(project.members or [])


def _docs_released(project: CompanyProject) -> bool:
    """Docs release once the required headcount has joined."""
    return _member_count(project) >= project.required_people


def _effective_deadline(project: CompanyProject):
    """Scheduled deadline plus approved extensions (max 4 weeks each)."""
    if not project.deadline:
        return None
    extra = sum(
        (ext.requested_days for ext in (project.deadline_extensions or [])
         if ext.status == "approved"),
        0,
    )
    return project.deadline + timedelta(days=extra)


def _project_payload(project: CompanyProject, db_members: list = None,
                     include_internal: bool = True,
                     viewer_role: str = "member") -> dict:
    """Serialize a project.

    - ``include_internal=False`` (customer gallery) omits help requests and
      member email details.
    - ``viewer_role`` controls the scope embedded in signed download URLs so
      investors/customers cannot open files they are not entitled to.
    """
    members = db_members if db_members is not None else (project.members or [])
    member_list = [{
        "id": m.id,
        "user_id": m.user_id,
        "name": f"{m.user.first_name} {m.user.last_name}".strip() if m.user else "—",
        "username": m.user.username if m.user else None,
        "role": m.role,
        "is_team_leader": m.is_team_leader,
        "joined_at": m.joined_at,
    } for m in members]

    doc_scope = "member" if viewer_role == "member" else viewer_role
    docs = [{
        "id": d.id,
        "filename": d.filename,
        "doc_type": d.doc_type,
        "uploaded_by": d.uploaded_by,
        "created_at": d.created_at,
        "download_url": (
            f"/api/v1/portal/projects/{project.id}/documents/{d.id}/download"
            f"?token={_sign_scope(f'doc:{project.id}:{d.id}:{doc_scope}')}"
        ),
    } for d in (project.documents or [])]

    # Software releases: only active ones; customers see download links for
    # published projects only (the download endpoint enforces this too).
    release_scope = "customer" if viewer_role == "customer" else "member"
    releases = [{
        "id": rel.id,
        "filename": rel.filename,
        "version": rel.version,
        "platform": rel.platform,
        "file_size": rel.file_size,
        "downloads": rel.downloads,
        "created_at": rel.created_at,
        "download_url": (
            f"/api/v1/portal/projects/{project.id}/releases/{rel.id}/download"
            f"?token={_sign_scope(f'release:{project.id}:{rel.id}:{release_scope}')}"
        ),
    } for rel in (project.releases or []) if rel.is_active]

    reports = sorted((project.progress_reports or []), key=lambda r: r.created_at)
    latest = reports[-1] if reports else None
    # The admin's grade is the official number; the leader-reported value is
    # shown until an admin grades the report.
    latest_percentage = None
    if latest:
        latest_percentage = (
            float(latest.admin_percentage) if latest.admin_percentage is not None
            else float(latest.percentage)
        )

    extensions = (project.deadline_extensions or [])
    effective_deadline = _effective_deadline(project)
    payload = {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "category": project.category,
        "section": project.section,
        "product_status": project.product_status,
        "platform": project.platform,
        "required_people": project.required_people,
        "status": project.status,
        "lifecycle_stage": project.lifecycle_stage,
        "team_leader_id": project.team_leader_id,
        "budget": float(project.budget) if project.budget else None,
        "deadline": project.deadline,
        "effective_deadline": effective_deadline,
        "overdue": bool(
            effective_deadline and date.today() > effective_deadline
        ),
        "created_at": project.created_at,
        "member_count": len(member_list),
        "docs_released": _docs_released(project),
        "staffing_plan": [{
            "id": it.id,
            "position": it.position,
            "count_required": it.count_required,
            "skills": it.skills,
            "experience_level": it.experience_level,
            "availability": it.availability,
            "duration": it.duration,
        } for it in (project.staffing_plan or [])],
        "members": member_list,
        "documents": docs,
        "releases": releases,
        "progress_percentage": latest_percentage,
        "progress_reports": [{
            "id": r.id,
            "week_label": r.week_label,
            "percentage": float(r.percentage),
            "admin_percentage": (float(r.admin_percentage)
                                  if r.admin_percentage is not None else None),
            "graded_by": r.graded_by,
            "graded_at": r.graded_at,
            "summary": r.summary,
            "reported_by": r.reported_by,
            "created_at": r.created_at,
        } for r in reports],
    }
    if include_internal:
        payload["change_requests"] = [{
            "id": cr.id,
            "title": cr.title,
            "description": cr.description,
            "status": cr.status,
            "impact_analysis": cr.impact_analysis,
            "requested_by": cr.requested_by,
            "created_at": cr.created_at,
        } for cr in (project.change_requests or [])]
        payload["help_requests"] = [{
            "id": h.id,
            "filename": h.filename,
            "message": h.message,
            "status": h.status,
            "user_id": h.user_id,
            "created_at": h.created_at,
            "download_url": (
                f"/api/v1/portal/projects/{project.id}/help/{h.id}/download"
                f"?token={_sign_scope(f'help:{project.id}:{h.id}:member')}"
            ),
        } for h in (project.help_requests or [])]
        payload["deadline_extensions"] = [{
            "id": e.id,
            "requested_days": e.requested_days,
            "reason": e.reason,
            "status": e.status,
            "requested_by": e.requested_by,
            "created_at": e.created_at,
        } for e in extensions]
    return payload


async def _get_project(db: AsyncSession, project_id: str) -> CompanyProject:
    from sqlalchemy.orm import selectinload
    result = await db.execute(
        select(CompanyProject)
        .options(
            selectinload(CompanyProject.members).selectinload(ProjectMember.user),
            selectinload(CompanyProject.documents),
            selectinload(CompanyProject.progress_reports),
            selectinload(CompanyProject.help_requests),
            selectinload(CompanyProject.deadline_extensions),
            selectinload(CompanyProject.staffing_plan),
            selectinload(CompanyProject.change_requests),
            selectinload(CompanyProject.releases),
        )
        .where(CompanyProject.id == project_id)
        .execution_options(populate_existing=True)
    )
    return result.scalar_one_or_none()


async def _active_project_count(db: AsyncSession, user_id: int) -> int:
    result = await db.execute(
        select(func.count())
        .select_from(ProjectMember)
        .join(CompanyProject, CompanyProject.id == ProjectMember.project_id)
        .where(
            ProjectMember.user_id == user_id,
            CompanyProject.status.in_(["open", "in_progress"]),
        )
    )
    return result.scalar() or 0


# ---------------------------------------------------------------------------
# Listing
# ---------------------------------------------------------------------------
@router.get("/projects")
async def list_projects(
    status_filter: Optional[str] = None,
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_member_or_investor),
    db: AsyncSession = Depends(get_db),
):
    """
    List projects. Developers see full detail; pure investors get a
    read-only progress view (no member/upload actions).
    """
    from sqlalchemy.orm import selectinload

    query = (
        select(CompanyProject)
        .options(
            selectinload(CompanyProject.members).selectinload(ProjectMember.user),
            selectinload(CompanyProject.documents),
            selectinload(CompanyProject.progress_reports),
            selectinload(CompanyProject.help_requests),
            selectinload(CompanyProject.deadline_extensions),
            selectinload(CompanyProject.staffing_plan),
            selectinload(CompanyProject.change_requests),
            selectinload(CompanyProject.releases),
        )
    )
    if status_filter:
        query = query.where(CompanyProject.status == status_filter)
    if category:
        query = query.where(CompanyProject.category == category)

    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(
        query.order_by(CompanyProject.created_at.desc())
        .offset((page - 1) * limit).limit(limit)
    )
    projects = result.scalars().all()

    investor_only = current_user.role == "investor"
    viewer_role = "investor" if investor_only else "member"
    return {
        "projects": [_project_payload(p, viewer_role=viewer_role) for p in projects],
        "investor_read_only": investor_only,
        "pagination": {"total": total, "page": page, "limit": limit,
                       "pages": (total + limit - 1) // limit if total else 0},
    }


# Literal route - MUST be declared before /projects/{project_id}.
@router.get("/projects/published")
async def list_published_projects(
    section: Optional[str] = Query(None),
    current_user: User = Depends(require_authenticated),
    db: AsyncSession = Depends(get_db),
):
    """Published company projects - the customer gallery (any logged-in user).
    Optionally filtered by gallery section; returns the list of available
    sections so the frontend can render section tabs."""
    from sqlalchemy.orm import selectinload

    sections_result = await db.execute(
        select(CompanyProject.section)
        .where(CompanyProject.status == "published")
        .distinct()
    )
    sections = sorted(
        s for (s,) in sections_result.all() if s
    )
    # Keep a stable, meaningful order: known sections first, then others.
    ordered = [s for s in PUBLISH_SECTIONS if s in sections]
    ordered += [s for s in sections if s not in ordered]

    query = (
        select(CompanyProject)
        .options(
            selectinload(CompanyProject.members).selectinload(ProjectMember.user),
            selectinload(CompanyProject.documents),
            selectinload(CompanyProject.progress_reports),
            selectinload(CompanyProject.deadline_extensions),
            selectinload(CompanyProject.staffing_plan),
            selectinload(CompanyProject.change_requests),
            selectinload(CompanyProject.releases),
        )
        .where(CompanyProject.status == "published")
    )
    if section:
        query = query.where(CompanyProject.section == section)
    result = await db.execute(query.order_by(CompanyProject.created_at.desc()))
    projects = result.scalars().all()
    return {
        "sections": ordered,
        "projects": [_project_payload(p, include_internal=False,
                                       viewer_role="customer")
                      for p in projects],
    }


@router.get("/projects/{project_id}")
async def get_project(
    project_id: str,
    current_user: User = Depends(require_member_or_investor),
    db: AsyncSession = Depends(get_db),
):
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    viewer_role = "investor" if current_user.role == "investor" else "member"
    return _project_payload(project, viewer_role=viewer_role)


# ---------------------------------------------------------------------------
# Joining a project (developers)
# ---------------------------------------------------------------------------
@router.post("/projects/{project_id}/join", status_code=status.HTTP_201_CREATED)
async def join_project(
    project_id: str,
    role: Optional[str] = None,
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    """A developer joins an open project (respects headcount + 3-project cap)."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.status not in ("open", "in_progress"):
        raise HTTPException(status_code=400, detail="This project is not accepting new members")

    # Already a member?
    existing = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project.id,
            ProjectMember.user_id == current_user.id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="You have already joined this project")

    # 3-project cap.
    active = await _active_project_count(db, current_user.id)
    if active >= MAX_PROJECTS_PER_DEVELOPER:
        raise HTTPException(
            status_code=400,
            detail=f"You are already on {MAX_PROJECTS_PER_DEVELOPER} active projects "
                   "(the maximum). Leave one before joining another.",
        )

    # Count members in the DB (the relationship collection loaded earlier is
    # stale until refresh, so don't trust _member_count() here).
    existing_count = await db.scalar(
        select(func.count())
        .select_from(ProjectMember)
        .where(ProjectMember.project_id == project.id)
    )
    is_first = existing_count == 0

    member = ProjectMember(
        project_id=project.id,
        user_id=current_user.id,
        role=role or "developer",
        is_team_leader=is_first and project.team_leader_id is None,
    )
    db.add(member)
    await db.flush()

    # First joiner becomes team leader if none set (persist team_leader_id).
    if project.team_leader_id is None and is_first:
        project.team_leader_id = current_user.id
        member.is_team_leader = True

    # Headcount reached -> move to in_progress and release docs.
    new_count = await db.scalar(
        select(func.count())
        .select_from(ProjectMember)
        .where(ProjectMember.project_id == project.id)
    )
    if new_count >= project.required_people and project.status == "open":
        project.status = "in_progress"

    await db.commit()

    # Reload so members/headcount reflect the new join (relationship was
    # loaded before the member was added).
    fresh = await _get_project(db, project.id)
    return {
        "message": "You have joined the project",
        "docs_released": _docs_released(fresh or project),
        "member_count": _member_count(fresh or project),
        "required_people": project.required_people,
        "is_team_leader": member.is_team_leader,
    }


@router.post("/projects/{project_id}/leave")
async def leave_project(
    project_id: str,
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project.id,
            ProjectMember.user_id == current_user.id,
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=400, detail="You are not a member of this project")

    await db.delete(member)
    # Reassign team leader to the first remaining member if needed.
    if project.team_leader_id == current_user.id:
        remaining = await db.execute(
            select(ProjectMember).where(ProjectMember.project_id == project.id)
        )
        next_members = remaining.scalars().all()
        if next_members:
            project.team_leader_id = next_members[0].user_id
            next_members[0].is_team_leader = True
        else:
            project.team_leader_id = None
    await db.commit()
    return {"message": "You have left the project"}


# ---------------------------------------------------------------------------
# Roles & team leader (members, admin override)
# ---------------------------------------------------------------------------
class RoleUpdate(BaseModel):
    role: str = Field(..., min_length=1, max_length=100)
    is_team_leader: bool = False


async def _require_member_or_admin(db, project: CompanyProject, user: User):
    if user.role == "admin":
        return
    result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project.id,
            ProjectMember.user_id == user.id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="You are not a member of this project")


@router.put("/projects/{project_id}/members/{member_id}/role")
async def update_member_role(
    project_id: str,
    member_id: str,
    body: RoleUpdate,
    current_user: User = Depends(require_role(["developer", "admin"])),
    db: AsyncSession = Depends(get_db),
):
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await _require_member_or_admin(db, project, current_user)

    result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.id == member_id,
            ProjectMember.project_id == project.id,
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    member.role = body.role
    if body.is_team_leader:
        # Demote any existing leader.
        others = await db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project.id,
                ProjectMember.is_team_leader == True,
            )
        )
        for o in others.scalars().all():
            o.is_team_leader = False
        member.is_team_leader = True
        project.team_leader_id = member.user_id

    await db.commit()
    return {"message": "Role updated", "role": member.role, "is_team_leader": member.is_team_leader}


# ---------------------------------------------------------------------------
# Extra developer requests
# ---------------------------------------------------------------------------
class ExtraDevRequest(BaseModel):
    # Upper bound is enforced in the endpoint (friendly 400 message) rather
    # than Pydantic (which would surface as a bare 422).
    requested_count: int = Field(1, ge=1)
    reason: Optional[str] = None


@router.post("/projects/{project_id}/request-extra", status_code=status.HTTP_201_CREATED)
async def request_extra_developers(
    project_id: str,
    body: ExtraDevRequest,
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    """A member requests extra developers (max 3) when the work is overwhelming."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await _require_member_or_admin(db, project, current_user)

    if body.requested_count > MAX_EXTRA_DEVELOPERS:
        raise HTTPException(
            status_code=400,
            detail=f"You may request at most {MAX_EXTRA_DEVELOPERS} extra developers",
        )

    req = ExtraDeveloperRequest(
        project_id=project.id,
        requested_by=current_user.id,
        requested_count=body.requested_count,
        reason=body.reason,
    )
    db.add(req)
    await db.commit()
    return {"message": "Extra developer request submitted for admin approval", "id": req.id}


# ---------------------------------------------------------------------------
# Weekly progress reports (team leader) - visible to investors + admin
# ---------------------------------------------------------------------------
class ProgressReportIn(BaseModel):
    week_label: str = Field(..., min_length=1, max_length=50)
    percentage: float = Field(..., ge=0, le=100)
    summary: Optional[str] = Field(None, max_length=5000)


@router.post("/projects/{project_id}/progress", status_code=status.HTTP_201_CREATED)
async def submit_progress_report(
    project_id: str,
    body: ProgressReportIn,
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    """The team leader submits the weekly progress report (graded %)."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await _require_member_or_admin(db, project, current_user)

    if current_user.role != "admin":
        result = await db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project.id,
                ProjectMember.user_id == current_user.id,
                ProjectMember.is_team_leader == True,  # noqa: E712
            )
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=403,
                detail="Only the team leader can submit the weekly progress report",
            )

    # One report per week label (keeps progress_percentage unambiguous).
    existing = await db.scalar(
        select(func.count())
        .select_from(ProjectProgressReport)
        .where(
            ProjectProgressReport.project_id == project.id,
            ProjectProgressReport.week_label == body.week_label,
        )
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"A progress report for '{body.week_label}' already exists",
        )

    report = ProjectProgressReport(
        project_id=project.id,
        reported_by=current_user.id,
        week_label=body.week_label,
        percentage=body.percentage,
        summary=body.summary,
    )
    db.add(report)
    await db.commit()
    return {
        "message": "Weekly progress report submitted",
        "id": report.id,
        "percentage": body.percentage,
    }


class ProgressGradeIn(BaseModel):
    admin_percentage: float = Field(..., ge=0, le=100)


@router.post("/projects/{project_id}/progress/{report_id}/grade")
async def grade_progress_report(
    project_id: str,
    report_id: str,
    body: ProgressGradeIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Admin grades a weekly progress report - the official percentage
    investors see (until graded, the leader-reported value is shown)."""
    report = await db.scalar(
        select(ProjectProgressReport).where(
            ProjectProgressReport.id == report_id,
            ProjectProgressReport.project_id == project_id,
        )
    )
    if not report:
        raise HTTPException(status_code=404, detail="Progress report not found")
    report.admin_percentage = body.admin_percentage
    report.graded_by = current_user.id
    report.graded_at = datetime.now()
    await db.commit()
    return {
        "message": "Progress report graded",
        "id": report.id,
        "admin_percentage": body.admin_percentage,
    }


@router.get("/projects/{project_id}/progress")
async def get_progress_reports(
    project_id: str,
    current_user: User = Depends(require_member_or_investor),
    db: AsyncSession = Depends(get_db),
):
    """Progress history for a project (members, investors, admin)."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    reports = sorted((project.progress_reports or []), key=lambda r: r.created_at)
    return {"reports": [{
        "id": r.id,
        "week_label": r.week_label,
        "percentage": float(r.percentage),
        "admin_percentage": (float(r.admin_percentage)
                              if r.admin_percentage is not None else None),
        "graded_by": r.graded_by,
        "graded_at": r.graded_at,
        "summary": r.summary,
        "reported_by": r.reported_by,
        "created_at": r.created_at,
    } for r in reports]}


# ---------------------------------------------------------------------------
# Deadline extensions (max 4 weeks; admin approves)
# ---------------------------------------------------------------------------
class DeadlineExtensionIn(BaseModel):
    requested_days: int = Field(1, ge=1, le=MAX_EXTENSION_DAYS)
    reason: str = Field(..., min_length=5, max_length=2000)


@router.post("/projects/{project_id}/extension", status_code=status.HTTP_201_CREATED)
async def request_deadline_extension(
    project_id: str,
    body: DeadlineExtensionIn,
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    """The team leader requests a deadline extension (max 4 weeks from the
    scheduled deadline) when the project cannot be completed in time."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await _require_member_or_admin(db, project, current_user)

    if current_user.role != "admin":
        result = await db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project.id,
                ProjectMember.user_id == current_user.id,
                ProjectMember.is_team_leader == True,  # noqa: E712
            )
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=403,
                detail="Only the team leader can request a deadline extension",
            )

    if not project.deadline:
        raise HTTPException(
            status_code=400,
            detail="This project has no scheduled deadline to extend",
        )

    pending = await db.scalar(
        select(func.count())
        .select_from(ProjectDeadlineExtension)
        .where(
            ProjectDeadlineExtension.project_id == project.id,
            ProjectDeadlineExtension.status == "pending",
        )
    )
    if pending:
        raise HTTPException(
            status_code=400,
            detail="A deadline extension request is already pending admin approval",
        )

    ext = ProjectDeadlineExtension(
        project_id=project.id,
        requested_by=current_user.id,
        requested_days=body.requested_days,
        reason=body.reason,
    )
    db.add(ext)
    await db.commit()
    return {
        "message": f"Extension request of {body.requested_days} day(s) submitted "
                   "for admin approval",
        "id": ext.id,
    }


# ---------------------------------------------------------------------------
# Developer help requests (upload own project docs for help, anytime)
# ---------------------------------------------------------------------------
@router.post("/projects/{project_id}/help", status_code=status.HTTP_201_CREATED)
async def submit_help_request(
    project_id: str,
    request: Request,
    file: UploadFile = File(...),
    message: str = Form(None),
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    """A developer uploads a document about their work to ask for help, anytime."""
    # Uploads write to disk - keep them throttled (disk-fill hardening).
    check_rate_limit(request, f"help_upload:user:{current_user.id}",
                     max_hits=10, window_seconds=3600)

    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await _require_member_or_admin(db, project, current_user)

    stored_path = await _save_upload(file, "help")
    req = ProjectHelpRequest(
        project_id=project.id,
        user_id=current_user.id,
        filename=file.filename or "document",
        stored_path=stored_path,
        message=message,
        status="open",
    )
    db.add(req)
    await db.commit()
    return {
        "message": "Help request submitted - an admin will review it",
        "id": req.id,
    }


@router.get("/projects/{project_id}/help")
async def get_help_requests(
    project_id: str,
    current_user: User = Depends(require_role(["developer", "admin"])),
    db: AsyncSession = Depends(get_db),
):
    """List help requests for a project (members + admin)."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await _require_member_or_admin(db, project, current_user)
    return {"requests": [{
        "id": h.id,
        "filename": h.filename,
        "message": h.message,
        "status": h.status,
        "user_id": h.user_id,
        "created_at": h.created_at,
    } for h in (project.help_requests or [])]}


# ---------------------------------------------------------------------------
# Documents: upload completed work (members) / download spec
# ---------------------------------------------------------------------------
def _safe_download_path(stored_path: str) -> str:
    """Resolve a stored upload path, refusing path traversal outside UPLOAD_DIR."""
    base = os.path.realpath(settings.UPLOAD_DIR)
    full = os.path.realpath(stored_path)
    if os.path.commonpath([base, full]) != base:
        raise HTTPException(status_code=400, detail="Invalid document path")
    if not os.path.isfile(full):
        raise HTTPException(status_code=404, detail="Document file not found")
    return full


@router.get("/projects/{project_id}/documents/{document_id}/download")
async def download_project_document(
    project_id: str,
    document_id: str,
    token: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Download a project document (spec / completed work).

    Works two ways:
    - Bearer token (members/admins/investors with the existing role rules), or
    - a short-lived signed URL (``?token=``) issued in the project payload,
      scoped to the viewer class (member / investor / customer) so investors
      cannot open locked or completed-work docs and customers can only open
      docs of published projects.
    """
    from fastapi.responses import FileResponse

    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    doc = next(
        (d for d in (project.documents or []) if str(d.id) == str(document_id)),
        None,
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    scope_class = None
    if token:
        scope = _resource_from_token(token)
        expected_prefix = f"doc:{project_id}:{document_id}:"
        if not scope or not scope.startswith(expected_prefix):
            raise HTTPException(status_code=403, detail="Invalid or expired download link")
        scope_class = scope[len(expected_prefix):]
    elif current_user:
        scope_class = "investor" if current_user.role == "investor" else "member"
    else:
        raise HTTPException(
            status_code=401,
            detail="Authentication required - sign in or use the download link",
        )

    if scope_class == "investor":
        if not project.docs_released:
            raise HTTPException(
                status_code=403,
                detail="Documentation is locked until the team is full",
            )
        if doc.doc_type == "completed":
            raise HTTPException(
                status_code=403,
                detail="Completed-work documents are not available to investors",
            )
    elif scope_class == "customer" and project.status != "published":
        raise HTTPException(
            status_code=403,
            detail="This document is only available for published projects",
        )

    path = _safe_download_path(doc.stored_path)
    return FileResponse(path, filename=doc.filename or os.path.basename(path))


@router.get("/projects/{project_id}/help/{help_id}/download")
async def download_help_document(
    project_id: str,
    help_id: str,
    token: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Download a developer's help-request document (members + admin)."""
    from fastapi.responses import FileResponse

    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    req = next(
        (h for h in (project.help_requests or []) if str(h.id) == str(help_id)),
        None,
    )
    if not req:
        raise HTTPException(status_code=404, detail="Help request not found")

    if token:
        scope = _resource_from_token(token)
        expected_prefix = f"help:{project_id}:{help_id}:"
        if not scope or not scope.startswith(expected_prefix):
            raise HTTPException(status_code=403, detail="Invalid or expired download link")
        if scope[len(expected_prefix):] != "member":
            raise HTTPException(status_code=403, detail="Invalid or expired download link")
    elif current_user:
        if current_user.role not in ("developer", "admin"):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        await _require_member_or_admin(db, project, current_user)
    else:
        raise HTTPException(
            status_code=401,
            detail="Authentication required - sign in or use the download link",
        )

    path = _safe_download_path(req.stored_path)
    return FileResponse(path, filename=req.filename or os.path.basename(path))


async def _save_upload(file: UploadFile, subdir: str) -> str:
    if file.content_type not in ALLOWED_DOC_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"File type '{file.content_type}' is not allowed (PDF/DOCX/text/images)",
        )
    contents = await file.read()
    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the {settings.MAX_FILE_SIZE // (1024 * 1024)}MB limit",
        )
    ext = os.path.splitext(file.filename or "file")[1]
    stored_name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(settings.UPLOAD_DIR, "projects", subdir, stored_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(contents)
    return path


async def _save_release(file: UploadFile) -> str:
    """Save a software build (.apk, .zip, .exe, ...). Validated by extension
    because browsers send unreliable MIME types for binaries. Served only as
    an attachment download, never inline."""
    name = file.filename or "release.bin"
    lower = name.lower()
    allowed = any(lower.endswith(ext) for ext in ALLOWED_RELEASE_EXTENSIONS)
    if not allowed:
        raise HTTPException(
            status_code=415,
            detail=(
                "File type not allowed for software releases. Allowed: "
                + ", ".join(sorted(ALLOWED_RELEASE_EXTENSIONS))
            ),
        )
    contents = await file.read()
    if len(contents) > settings.MAX_RELEASE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the {settings.MAX_RELEASE_SIZE // (1024 * 1024)}MB release limit",
        )
    ext = os.path.splitext(name)[1]
    stored_name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(settings.UPLOAD_DIR, "projects", "releases", stored_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(contents)
    return path


@router.get("/projects/{project_id}/releases/{release_id}/download")
async def download_project_release(
    project_id: str,
    release_id: str,
    token: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Download a software build (.apk/.zip/...).

    Customers use the short-lived signed URL from the published gallery
    (scoped ``release:<project>:<release>:customer``); only downloads of
    active releases on *published* projects are allowed for that class.
    Members/admins can download with their normal login for any status.
    Served as an attachment so it can never execute in the browser."""
    from fastapi.responses import FileResponse

    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    release = next(
        (rel for rel in (project.releases or []) if str(rel.id) == str(release_id)),
        None,
    )
    if not release or not release.is_active:
        raise HTTPException(status_code=404, detail="Release not found")

    scope_class = None
    if token:
        scope = _resource_from_token(token)
        expected_prefix = f"release:{project_id}:{release_id}:"
        if not scope or not scope.startswith(expected_prefix):
            raise HTTPException(status_code=403, detail="Invalid or expired download link")
        scope_class = scope[len(expected_prefix):]
    elif current_user:
        scope_class = "investor" if current_user.role == "investor" else "member"
    else:
        raise HTTPException(
            status_code=401,
            detail="Authentication required - sign in or use the download link",
        )

    if scope_class == "customer":
        if project.status != "published":
            raise HTTPException(
                status_code=403,
                detail="This software is only available for published projects",
            )
    elif scope_class == "investor":
        if project.status != "published":
            raise HTTPException(
                status_code=403,
                detail="Investors can only download software of published projects",
            )

    path = _safe_download_path(release.stored_path)
    release.downloads = (release.downloads or 0) + 1
    await db.commit()
    return FileResponse(
        path,
        filename=release.filename or os.path.basename(path),
        media_type="application/octet-stream",
        content_disposition_type="attachment",
    )


@router.post("/projects/{project_id}/upload", status_code=status.HTTP_201_CREATED)
async def upload_project_document(
    project_id: str,
    file: UploadFile = File(...),
    doc_type: str = Query("completed", pattern="^(completed|review)$"),
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    """Members upload completed work for admin review (default doc_type=completed).
    Uploads are blocked once the (effective) deadline has passed - the team
    must first request an approved extension (max 4 weeks)."""
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await _require_member_or_admin(db, project, current_user)

    effective = _effective_deadline(project)
    if effective and date.today() > effective:
        raise HTTPException(
            status_code=400,
            detail="The project deadline has passed. The team leader must request "
                   "a deadline extension (max 4 weeks) for the work to be accepted.",
        )

    stored_path = await _save_upload(file, "completed")
    doc = ProjectDocument(
        project_id=project.id,
        filename=file.filename or "document",
        stored_path=stored_path,
        doc_type=doc_type,
        uploaded_by=current_user.id,
    )
    db.add(doc)
    await db.flush()
    if project.status in ("open", "in_progress"):
        project.status = "review"
    await db.commit()
    return {"message": "Work uploaded for review", "document_id": doc.id}


# ---------------------------------------------------------------------------
# Project chat + AI help
# ---------------------------------------------------------------------------
class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    ask_ai: bool = False


@router.get("/projects/{project_id}/chat")
async def get_project_chat(
    project_id: str,
    current_user: User = Depends(require_member_or_investor),
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy.orm import selectinload
    project = await db.scalar(
        select(CompanyProject).where(CompanyProject.id == project_id)
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    result = await db.execute(
        select(ProjectChatMessage)
        .options(selectinload(ProjectChatMessage.user))
        .where(ProjectChatMessage.project_id == project.id)
        .order_by(ProjectChatMessage.created_at.asc())
        .limit(200)
    )
    messages = result.scalars().all()
    return {"messages": [{
        "id": m.id,
        "user_id": m.user_id,
        "sender": f"{m.user.first_name} {m.user.last_name}".strip() if m.user else "N.O.U Lite AI",
        "username": m.user.username if m.user else None,
        "message": m.message,
        "is_ai": m.is_ai,
        "created_at": m.created_at,
    } for m in messages]}


@router.post("/projects/{project_id}/chat", status_code=status.HTTP_201_CREATED)
async def post_project_chat(
    project_id: str,
    body: ChatMessage,
    request: Request,
    current_user: User = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    """Post a message to the project chat; optionally get an AI reply (Groq pool)."""
    if body.ask_ai:
        # AI calls draw from the shared Groq pool - keep the section from
        # being exhausted by a single chatty member.
        check_rate_limit(request, f"project_ai:user:{current_user.id}",
                         max_hits=30, window_seconds=3600)
    project = await _get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await _require_member_or_admin(db, project, current_user)

    chat = ProjectChatMessage(
        project_id=project.id,
        user_id=current_user.id,
        message=body.message,
        is_ai=False,
    )
    db.add(chat)
    await db.flush()

    ai_reply = None
    if body.ask_ai:
        ai_reply = await _call_project_ai(db, project, body.message, current_user)

    await db.commit()
    return {
        "message": "Message posted",
        "chat_id": chat.id,
        "ai_reply": ai_reply,
    }


async def _call_project_ai(db, project: CompanyProject, question: str, user: User) -> dict:
    """Ask the AI (Groq via key pool) about the project - bugs, design, etc."""
    from app.services.groq_pool import get_client, mark_failed
    from groq import AuthenticationError

    try:
        client, key_index = await get_client("project_chat")
    except RuntimeError as exc:
        return {"error": str(exc)}

    system_prompt = (
        "You are N.O.U Lite AI, the engineering assistant inside the N.O.U "
        "Digital Systems project portal. Developers working on the project "
        f"'{project.title}' (category: {project.category or 'general'}) ask "
        "you about bugs, architecture, and implementation problems. Be "
        "practical, concrete and concise. You may suggest code, debugging "
        "steps, or design trade-offs. Do not claim to have access to their "
        "private files - answer from general engineering knowledge."
    )
    try:
        resp = await client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.4,
            max_tokens=900,
        )
        answer = (resp.choices[0].message.content or "").strip()
    except AuthenticationError:
        mark_failed("project_chat", key_index)
        return {"error": "AI temporarily unavailable (key rotation). Try again."}
    except Exception as exc:  # noqa: BLE001
        return {"error": f"AI unavailable: {str(exc)[:150]}"}

    ai_msg = ProjectChatMessage(
        project_id=project.id,
        user_id=None,
        message=answer,
        is_ai=True,
    )
    db.add(ai_msg)
    await db.flush()
    return {"message": answer, "chat_id": ai_msg.id}
