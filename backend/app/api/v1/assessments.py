"""
Assessments API endpoints.

Implements the N.O.U. Employment Assessment Framework (today.md):

- Five-part assessment: Common -> Category -> Position -> Practical -> Professional
- NO multiple-choice questions. Question types: short_answer, written_explanation,
  scenario, practical, debugging, design, project.
- Configurable per-category weights (defaults: logic 15%, general 5%,
  category 25%, position 25%, practical 25%, professional 5%).
- Competency classification: 0-49 Not Qualified, 50-64 Developing, 65-79
  Competent, 80-89 N.O.U. Qualified, 90-100 Advanced.
- Question banks per module (AI generates a fresh randomized set per session).
- Alternative category recommendation when the applicant does not qualify.

The applicant first selects a professional category + position (personnel
API), then starts the assessment. Groq pre-generates a 100-question bank per
category (stored in question_bank); each assessment instantly draws 20 random
questions from it, and Groq grades the written answers afterwards.
"""

import json
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.assessment_framework import (
    PARTS,
    PART_QUESTION_TYPES,
    QUESTIONS_PER_PART,
    ASSESSMENT_DURATION_MINUTES,
    QUALIFYING_PERCENT,
    BANK_QUESTIONS_PER_PART,
    competency_band,
    qualifies,
    weighted_percentage,
    recommend_alternative,
)
from app.core.database import get_db
from app.core.rate_limit import check_rate_limit
from app.core.security import (
    get_current_user,
    get_optional_user,
    require_applicant,
    get_password_hash,
)
from app.models.user import User
from app.models.personnel import PersonnelCategory, PersonnelPosition
from app.models.assessment import (
    Assessment,
    AssessmentSession,
    AssessmentAnswer,
    AssessmentSessionQuestion,
)
from app.services import ai_assessment
from app.services.question_bank import ensure_bank, pick_questions
from app.services.assessment_results import build_session_feedback
from app.services.watermark import embed_watermark, generate_watermark

router = APIRouter()


class AnswerItem(BaseModel):
    # Question ids are ints in the DB but are serialised as strings in some
    # API responses - accept both so the submit payload is robust.
    question_id: str
    user_answer: Optional[str] = None

    @field_validator("question_id", mode="before")
    @classmethod
    def coerce_question_id(cls, value: object) -> str:
        return str(value)


class SubmitAssessmentRequest(BaseModel):
    answers: List[AnswerItem]


class StartAssessmentRequest(BaseModel):
    # Professional category + position the applicant is applying for.
    category_id: int
    position_id: int
    # Guest assessment (no login): the applicant identifies by email. The
    # applicant record is created on the fly if it does not exist yet, so the
    # assessment is fully open - no account or login is required.
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=120)
    phone: Optional[str] = Field(None, max_length=30)


class GuestIdentity(BaseModel):
    email: Optional[EmailStr] = None


async def _resolve_applicant(
    db: AsyncSession,
    current_user: Optional[User],
    email: Optional[str],
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
) -> User:
    """
    Return the applicant user for a request.

    - Authenticated applicant/admin -> their own record.
    - Guest -> find the applicant by email (created by the public apply form)
      or create a minimal applicant profile on the fly so the assessment is
      open to anyone. Guests cannot log in (no password is set) - credentials
      are only issued later by the admin for those who qualify.
    """
    if current_user is not None and current_user.role in ("applicant", "admin"):
        return current_user

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide your email to start the assessment",
        )

    normalized = email.strip().lower()
    user = await db.scalar(select(User).where(User.email == normalized))
    if user:
        # Refresh the phone number if the applicant provided one (e.g. they
        # keyed it on the assessment page after applying via Careers).
        if phone:
            user.phone = phone
        return user

    parts = (full_name or normalized.split("@")[0]).strip().split(None, 1)
    user = User(
        email=normalized,
        password_hash=get_password_hash(__import__("secrets").token_hex(12)),
        first_name=parts[0] if parts else normalized.split("@")[0],
        last_name=parts[1] if len(parts) > 1 else "",
        role="applicant",
        is_active=True,
        phone=phone,
        terms_accepted_at=datetime.now(),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


# ---------------------------------------------------------------------------
# Framework / rules (for the assessment UI)
# ---------------------------------------------------------------------------
@router.get("/framework")
async def get_framework(
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Return the 5-part assessment framework + scoring rules for the UI."""
    return {
        "parts": [
            {
                "part": "common",
                "label": "Common Assessment",
                "description": (
                    "Logic & critical thinking and general computer / "
                    "professional knowledge - real-world problems, not puzzles."
                ),
                "types": PART_QUESTION_TYPES["common"],
                "questions": QUESTIONS_PER_PART["common"],
            },
            {
                "part": "category",
                "label": "Category Assessment",
                "description": "Knowledge of your selected professional field.",
                "types": PART_QUESTION_TYPES["category"],
                "questions": QUESTIONS_PER_PART["category"],
            },
            {
                "part": "position",
                "label": "Position Assessment",
                "description": "Knowledge specific to the position you applied for.",
                "types": PART_QUESTION_TYPES["position"],
                "questions": QUESTIONS_PER_PART["position"],
            },
            {
                "part": "practical",
                "label": "Practical Assessment",
                "description": "Perform an actual task - design, build or troubleshoot.",
                "types": PART_QUESTION_TYPES["practical"],
                "questions": QUESTIONS_PER_PART["practical"],
            },
            {
                "part": "professional",
                "label": "Professional Assessment",
                "description": "Communication, ethics, teamwork and professional judgement.",
                "types": PART_QUESTION_TYPES["professional"],
                "questions": QUESTIONS_PER_PART["professional"],
            },
        ],
        "question_types": [
            {"value": "short_answer", "label": "Short Answer"},
            {"value": "written_explanation", "label": "Written Explanation"},
            {"value": "scenario", "label": "Scenario"},
            {"value": "practical", "label": "Practical"},
            {"value": "debugging", "label": "Debugging"},
            {"value": "design", "label": "Design"},
            {"value": "project", "label": "Project"},
        ],
        "duration_minutes": ASSESSMENT_DURATION_MINUTES,
        "qualifying_percent": QUALIFYING_PERCENT,
        "competency_bands": [
            {"min": 90, "label": "Advanced"},
            {"min": 80, "label": "N.O.U. Qualified"},
            {"min": 65, "label": "Competent"},
            {"min": 50, "label": "Developing"},
            {"min": 0, "label": "Not Qualified"},
        ],
        "default_weights": {
            "logic": 15, "general": 5, "category": 25,
            "position": 25, "practical": 25, "professional": 5,
        },
    }


@router.get("/modules")
async def get_modules(
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Legacy endpoint kept for compatibility - returns the framework rules."""
    return await get_framework(current_user)


# ---------------------------------------------------------------------------
# Assessment listing / details
# ---------------------------------------------------------------------------
@router.get("/results/me")
async def get_my_results(
    current_user: User = Depends(require_applicant),
    db: AsyncSession = Depends(get_db),
):
    """Get current applicant's completed assessment results."""
    result = await db.execute(
        select(AssessmentSession)
        .where(
            AssessmentSession.applicant_id == current_user.id,
            AssessmentSession.status == "completed",
        )
        .order_by(AssessmentSession.completed_at.desc())
    )
    sessions = result.scalars().all()

    results = []
    for session in sessions:
        assessment = await db.scalar(
            select(Assessment).where(Assessment.id == session.assessment_id)
        )
        results.append({
            "id": session.id,
            "assessment": {"title": assessment.title if assessment else "Assessment"},
            "score": session.score,
            "percentage": session.percentage,
            "status": session.status,
            "completedAt": session.completed_at,
            "aiSummary": session.ai_summary,
            "aiRecommendation": session.ai_recommendation,
            "passed": session.ai_recommendation == "PASS",
            "modules": _parse_modules(session),
            "categoryName": session.category_name,
            "positionName": session.position_name,
            "partScores": _parse_part_scores(session),
            "competencyBand": session.competency_band,
            "recommendedCategory": session.recommended_category,
        })

    return {"results": results}


@router.get("/")
async def list_assessments(
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """List available assessments."""
    result = await db.execute(
        select(Assessment).where(Assessment.is_active == True)
    )
    return result.scalars().all()


# ---------------------------------------------------------------------------
# Active session (resume) - MUST be declared before /{assessment_id} so the
# literal "active" path is not captured as an assessment id.
# ---------------------------------------------------------------------------
@router.get("/active")
async def get_active_session(
    email: Optional[str] = None,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Return the applicant's in-progress assessment session (if any) with its
    questions, so a page refresh mid-exam can resume instead of locking the
    applicant out (start_assessment rejects a second start).
    """
    applicant = await _resolve_applicant(db, current_user, email)
    session = await db.scalar(
        select(AssessmentSession).where(
            AssessmentSession.applicant_id == applicant.id,
            AssessmentSession.status == "in_progress",
        ).order_by(AssessmentSession.started_at.desc()).limit(1)
    )
    if not session:
        return {"session": None, "questions": [], "questions_by_module": {}}

    sq_result = await db.execute(
        select(AssessmentSessionQuestion)
        .where(AssessmentSessionQuestion.session_id == session.id)
        .order_by(AssessmentSessionQuestion.order_number)
    )
    session_questions = sq_result.scalars().all()

    grouped: dict = {}
    flat = []
    for sq in session_questions:
        grouped.setdefault(sq.part or sq.module, []).append({
            "id": sq.id,
            "module": sq.module,
            "part": sq.part,
            "question_type": sq.question_type,
            "category": sq.category,
            "question_text": sq.question_text,
            "points": sq.points,
            "order_number": sq.order_number,
        })
        flat.append({"id": sq.id, "module": sq.module, "part": sq.part,
                     "question_type": sq.question_type, "category": sq.category,
                     "question_text": sq.question_text, "points": sq.points,
                     "order_number": sq.order_number})

    return {
        "session": {
            "id": session.id,
            "assessment_id": session.assessment_id,
            "time_remaining": session.time_remaining,
        },
        "questions": flat,
        "questions_by_module": grouped,
        "modules": _parse_modules(session),
        "categoryName": session.category_name,
        "positionName": session.position_name,
        "ai_generated": True,
        "source": "question_bank",
        "questions_total": sum(QUESTIONS_PER_PART.values()),
        "questions_per_part": dict(QUESTIONS_PER_PART),
    }


# ---------------------------------------------------------------------------
# Assessment listing / details
# ---------------------------------------------------------------------------
@router.get("/{assessment_id}")
async def get_assessment(
    assessment_id: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Get assessment details."""
    assessment = await db.scalar(
        select(Assessment).where(
            Assessment.id == assessment_id,
            Assessment.is_active == True,
        )
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return assessment


# ---------------------------------------------------------------------------
# Start / submit
# ---------------------------------------------------------------------------
def _parse_modules(session: AssessmentSession) -> List[str]:
    try:
        return json.loads(session.modules) if session.modules else []
    except (TypeError, ValueError):
        return []


def _parse_part_scores(session: AssessmentSession) -> dict:
    try:
        return json.loads(session.part_scores) if session.part_scores else {}
    except (TypeError, ValueError):
        return {}


def _category_weights(category: PersonnelCategory) -> dict:
    if not category:
        return {}
    return {
        "logic": category.weight_logic,
        "general": category.weight_general,
        "category": category.weight_category,
        "position": category.weight_position,
        "practical": category.weight_practical,
        "professional": category.weight_professional,
    }


@router.post("/{assessment_id}/start", status_code=status.HTTP_201_CREATED)
async def start_assessment(
    assessment_id: str,
    body: StartAssessmentRequest,
    request: Request,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Start a 5-part assessment session for the applicant's chosen professional
    category + position. The session is created INSTANTLY: the category's
    pre-generated question bank (100 questions, built once with Groq) is used
    to draw this applicant's randomized 20-question set. Groq is never called
    while the exam is running - it only grades the answers afterwards. No
    login required - guests identify by email.
    """
    # Rate-limit guest (unauthenticated) starts per IP to prevent abuse.
    if current_user is None:
        check_rate_limit(request, "guest-assessment:ip", max_hits=5, window_seconds=3600)

    applicant = await _resolve_applicant(db, current_user, body.email, body.full_name, body.phone)

    assessment = await db.scalar(
        select(Assessment).where(
            Assessment.id == assessment_id,
            Assessment.is_active == True,
        )
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    category = await db.scalar(
        select(PersonnelCategory).where(PersonnelCategory.id == body.category_id)
    )
    if not category or category.is_active != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please choose a valid professional category",
        )
    position = await db.scalar(
        select(PersonnelPosition).where(
            PersonnelPosition.id == body.position_id,
            PersonnelPosition.category_id == category.id,
        )
    )
    if not position or position.is_active != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please choose a valid position under the selected category",
        )

    # Only one active session per assessment.
    active = await db.scalar(
        select(AssessmentSession).where(
            AssessmentSession.applicant_id == applicant.id,
            AssessmentSession.assessment_id == assessment_id,
            AssessmentSession.status == "in_progress",
        )
    )
    if active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active session for this assessment",
        )

    # -------------------------------------------------------------------
    # Question bank: make sure the category's 100-question bank exists
    # (Groq generates it once, then it is stored), then draw THIS
    # applicant's randomized 20-question set instantly. No Groq call runs
    # during the exam, so every start is fast and never blank.
    # -------------------------------------------------------------------
    try:
        await ensure_bank(db, category, questions_per_part=BANK_QUESTIONS_PER_PART)
    except ai_assessment.AINotConfiguredError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )
    except ai_assessment.AIAPIError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )

    # Re-check for a concurrent active session: two parallel starts can both
    # pass the check above while the (potentially slow) bank generation lock
    # is held. Whoever creates the session first wins - the other must not
    # create a duplicate.
    active = await db.scalar(
        select(AssessmentSession).where(
            AssessmentSession.applicant_id == applicant.id,
            AssessmentSession.assessment_id == assessment_id,
            AssessmentSession.status == "in_progress",
        )
    )
    if active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active session for this assessment",
        )

    bank_questions = await pick_questions(db, category.id)

    # Module label used for display grouping.
    module_label = f"{category.name} / {position.name}"

    # Create the session IMMEDIATELY and snapshot the drawn questions into
    # it (order_number = exam order: common -> category -> position ->
    # practical -> professional).
    new_session = AssessmentSession(
        applicant_id=applicant.id,
        assessment_id=assessment_id,
        time_remaining=ASSESSMENT_DURATION_MINUTES * 60,
        status="in_progress",
        modules=json.dumps([module_label]),
        category_id=category.id,
        position_id=position.id,
        category_name=category.name,
        position_name=position.name,
    )
    db.add(new_session)
    await db.flush()
    await db.refresh(new_session)

    for order_number, bq in enumerate(bank_questions, start=1):
        # Each question carries its own invisible watermark token so a copied
        # question can be traced back to the AI tool that answered it.
        watermarked_text = embed_watermark(
            bq.question_text, generate_watermark()
        )
        db.add(AssessmentSessionQuestion(
            session_id=new_session.id,
            category=bq.category_name,
            module=module_label,
            part=bq.part,
            question_type=bq.question_type,
            question_text=watermarked_text,
            order_number=order_number,
            points=bq.points or 10,
            grading_notes=bq.grading_notes or "",
        ))

    # Commit *before* responding (see comment below).
    await db.commit()
    await db.refresh(new_session)

    sq_result = await db.execute(
        select(AssessmentSessionQuestion)
        .where(AssessmentSessionQuestion.session_id == new_session.id)
        .order_by(AssessmentSessionQuestion.order_number)
    )
    session_questions = sq_result.scalars().all()

    return {
        "session": {
            "id": new_session.id,
            "assessment_id": new_session.assessment_id,
            "time_remaining": new_session.time_remaining,
        },
        "questions": [_question_payload(q) for q in session_questions],
        "questions_by_module": {},
        "modules": [module_label],
        "categoryName": category.name,
        "positionName": position.name,
        "weights": _category_weights(category),
        "ai_generated": True,
        "source": "question_bank",
        "questions_total": len(session_questions),
        "questions_per_part": dict(QUESTIONS_PER_PART),
    }


# ---------------------------------------------------------------------------
# Session question lookup (questions come from the pre-generated bank)
# ---------------------------------------------------------------------------
def _question_payload(sq: AssessmentSessionQuestion) -> dict:
    return {
        "id": sq.id,
        "module": sq.module,
        "part": sq.part,
        "question_type": sq.question_type,
        "category": sq.category,
        "question_text": sq.question_text,
        "points": sq.points,
        "order_number": sq.order_number,
    }


@router.get("/sessions/{session_id}/question")
async def get_session_question(
    session_id: str,
    index: int = Query(0, ge=0),
    request: Request = None,
    email: Optional[str] = None,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Return the question at ``index`` (0-based) for the applicant's active
    session. Questions now come from the pre-generated question bank (all 20
    are snapshot into the session at start), so this is a simple stored
    lookup - no Groq call runs during the exam.
    """
    if current_user is None:
        check_rate_limit(request, "guest-assessment-question:ip", max_hits=120, window_seconds=3600)

    applicant = await _resolve_applicant(db, current_user, email)
    session = await db.scalar(
        select(AssessmentSession).where(
            AssessmentSession.id == session_id,
            AssessmentSession.applicant_id == applicant.id,
            AssessmentSession.status == "in_progress",
        )
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active assessment session not found",
        )

    order_number = index + 1
    stored = await db.scalar(
        select(AssessmentSessionQuestion).where(
            AssessmentSessionQuestion.session_id == session.id,
            AssessmentSessionQuestion.order_number == order_number,
        )
    )
    if not stored:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found for this session",
        )
    return {"index": index, "question": _question_payload(stored)}


class SubmitAssessmentRequestGuest(SubmitAssessmentRequest):
    # Guest submit: identify by email (used when no token is provided).
    email: Optional[EmailStr] = None


@router.post("/sessions/{session_id}/submit")
async def submit_assessment(
    session_id: str,
    body: SubmitAssessmentRequestGuest,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit assessment answers; Groq grades them. The session stores the
    weighted 5-part score, competency band, and PASS/FAIL verdict per the
    N.O.U. assessment framework (qualifying = 80%+). No login required -
    guests identify by email."""
    applicant = await _resolve_applicant(db, current_user, body.email)
    session = await db.scalar(
        select(AssessmentSession).where(
            AssessmentSession.id == session_id,
            AssessmentSession.applicant_id == applicant.id,
            AssessmentSession.status == "in_progress",
        )
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment session not found or not active",
        )

    assessment = await db.scalar(
        select(Assessment).where(Assessment.id == session.assessment_id)
    )
    duration_minutes = ASSESSMENT_DURATION_MINUTES

    # Server-side time enforcement (fixed 3h30m window from session start).
    started = session.started_at
    if started:
        deadline = started + timedelta(minutes=duration_minutes)
        if datetime.now() > deadline:
            session.status = "completed"
            await db.flush()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assessment time has expired",
            )

    # Load the session's questions.
    sq_result = await db.execute(
        select(AssessmentSessionQuestion)
        .where(AssessmentSessionQuestion.session_id == session_id)
        .order_by(AssessmentSessionQuestion.order_number)
    )
    session_questions = sq_result.scalars().all()
    if not session_questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This session has no questions to grade",
        )

    answers_map = {str(a.question_id): a.user_answer or "" for a in body.answers}

    try:
        grading = await ai_assessment.grade_answers(
            assessment_title=assessment.title if assessment else "Assessment",
            questions=session_questions,
            answers_map=answers_map,
        )
    except ai_assessment.AINotConfiguredError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )
    except ai_assessment.AIAPIError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )

    # Persist per-question answers.
    total_score = 0.0
    max_score = 0.0
    ai_detected_count = 0
    for index, sq in enumerate(session_questions):
        item = grading["results"][index]
        total_score += item["score"]
        max_score += item["max_score"]
        # Surface AI-assistance detection to the admin: prepend a marker to
        # the per-question AI feedback when Groq flagged the answer.
        feedback = item["feedback"]
        if item.get("ai_detected"):
            ai_detected_count += 1
            feedback = (
                f"[AI-ASSISTANCE DETECTED - confidence {item.get('ai_confidence', 0):.0f}%] "
                f"{feedback}".strip()
            )
            reason = (item.get("ai_reason") or "").strip()
            if reason:
                feedback = f"{feedback}\nAI flag reason: {reason}"
        db.add(AssessmentAnswer(
            session_id=session_id,
            session_question_id=sq.id,
            user_answer=answers_map.get(str(sq.id), ""),
            is_correct=item["score"] >= item["max_score"] * 0.5,
            points_earned=item["score"],
            ai_feedback=feedback,
        ))
    await db.flush()

    # Per-part breakdown.
    part_totals: dict = {}
    for index, sq in enumerate(session_questions):
        item = grading["results"][index]
        part = sq.part or "position"
        entry = part_totals.setdefault(part, {"score": 0.0, "max": 0.0})
        entry["score"] += item["score"]
        entry["max"] += item["max_score"]

    part_scores = {
        part: round((entry["score"] / entry["max"] * 100), 2) if entry["max"] else 0
        for part, entry in part_totals.items()
    }
    # Ensure all 5 parts are present.
    for part in PARTS:
        part_scores.setdefault(part, 0)

    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    band = competency_band(percentage)
    passed = qualifies(percentage)

    # Weighted percentage using the category weights (falls back to defaults).
    category = None
    weights = {}
    if session.category_id:
        category = await db.scalar(
            select(PersonnelCategory).where(PersonnelCategory.id == session.category_id)
        )
    if category:
        weights = _category_weights(category)
    weighted_pct = weighted_percentage(part_scores, weights)

    # Alternative category recommendation when the applicant does not qualify.
    recommended = ""
    if not passed:
        recommended = recommend_alternative(part_scores)

    recommendation = "PASS" if passed else "FAIL"

    # Build a human summary from the AI verdict + part scores.
    summary_parts = [grading["summary"] or ""]
    summary_parts.append(
        f"Overall {percentage:.1f}% (weighted {weighted_pct:.1f}%) - "
        f"qualifying requires {QUALIFYING_PERCENT}%. Competency: {band}."
    )
    if ai_detected_count:
        summary_parts.append(
            f"AI-assistance flagged in {ai_detected_count} of "
            f"{len(session_questions)} answers - admin review recommended."
        )
    if not passed and recommended:
        summary_parts.append(
            f"Recommended alternative category: {recommended}."
        )

    session.score = total_score
    session.percentage = weighted_pct
    session.completed_at = datetime.now()
    session.status = "completed"
    session.ai_summary = " ".join(p for p in summary_parts if p)
    session.ai_recommendation = recommendation
    session.part_scores = json.dumps(part_scores)
    session.competency_band = band
    session.recommended_category = recommended or None

    # Commit *before* responding (see comment below).
    await db.commit()

    return {
        "session_id": session_id,
        "score": total_score,
        "percentage": weighted_pct,
        "raw_percentage": round(percentage, 2),
        "total_questions": len(session_questions),
        "passed": passed,
        "recommendation": recommendation,
        "competency_band": band,
        "recommended_category": recommended,
        "part_scores": part_scores,
        "weights": weights,
        "module_breakdown": [
            {
                "part": part,
                "score": entry["score"],
                "max_score": entry["max"],
                "percentage": part_scores.get(part, 0),
            }
            for part, entry in part_totals.items()
        ],
        "time_taken": max(0, int((datetime.now() - started).total_seconds())) if started else 0,
        "ai_graded": True,
        "feedback": [
            {
                "question": sq.question_text,
                "module": sq.module,
                "part": sq.part,
                "question_type": sq.question_type,
                "category": sq.category,
                "points": sq.points,
                "user_answer": answers_map.get(str(sq.id), ""),
                "score": grading["results"][index]["score"],
                "max_score": sq.points,
                "feedback": grading["results"][index]["feedback"],
                "strengths": grading["results"][index]["strengths"],
                "improvements": grading["results"][index]["improvements"],
                "ai_detected": grading["results"][index].get("ai_detected", False),
                "ai_confidence": grading["results"][index].get("ai_confidence", 0),
                "ai_reason": grading["results"][index].get("ai_reason", ""),
            }
            for index, sq in enumerate(session_questions)
        ],
        "summary": session.ai_summary,
        "ai_detected_count": ai_detected_count,
        "recommendation_note": (
            f"Your results will be emailed to you. If you pass, an admin will "
            f"review your assessment and your login credentials will be "
            f"emailed to you after approval."
        ),
    }


@router.get("/sessions/{session_id}/results")
async def get_assessment_results(
    session_id: str,
    email: Optional[str] = None,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Get assessment results, including per-question AI feedback."""
    applicant = await _resolve_applicant(db, current_user, email)
    session = await db.scalar(
        select(AssessmentSession).where(
            AssessmentSession.id == session_id,
            AssessmentSession.applicant_id == applicant.id,
        )
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment session not found",
        )

    feedback = await build_session_feedback(db, session_id)
    return {
        "session": session,
        "feedback": feedback,
        "partScores": _parse_part_scores(session),
        "competencyBand": session.competency_band,
        "recommendedCategory": session.recommended_category,
        "categoryName": session.category_name,
        "positionName": session.position_name,
    }
