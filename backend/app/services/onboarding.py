"""
Developer onboarding service.

Applicants who pass the assessment threshold appear on the admin dashboard.
When the admin approves, we:
1. mark the session onboarding_status = approved,
2. set the user's role to "developer",
3. generate fresh login credentials (password),
4. email the results + the new credentials (which open the projects portal).
"""

import secrets
import string
import logging
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assessment import Assessment, AssessmentSession
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings
from app.services.email import send_email, onboarding_email_html

logger = logging.getLogger("onboarding")


def generate_temporary_password(length: int = 12) -> str:
    """Cryptographically random temp password with a mix of classes."""
    alphabet = string.ascii_letters + string.digits + "!@#$%"
    while True:
        pw = "".join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.isupper() for c in pw) and any(c.islower() for c in pw)
                and any(c.isdigit() for c in pw)):
            return pw


async def list_passed_candidates(
    db: AsyncSession,
    page: int = 1,
    limit: int = 20,
) -> dict:
    """
    Return completed assessment sessions with PASS recommendation whose
    onboarding status is still pending (awaiting admin decision).
    """
    query = (
        select(AssessmentSession)
        .options(
            selectinload(AssessmentSession.applicant),
            selectinload(AssessmentSession.assessment),
        )
        .where(
            AssessmentSession.status == "completed",
            AssessmentSession.ai_recommendation == "PASS",
            AssessmentSession.onboarding_status == "pending",
        )
    )
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(
        query.order_by(AssessmentSession.completed_at.desc())
        .offset((page - 1) * limit).limit(limit)
    )
    sessions = result.scalars().all()
    return {
        "candidates": [{
            "session_id": s.id,
            "applicant": {
                "id": s.applicant_id,
                "name": f"{s.applicant.first_name} {s.applicant.last_name}".strip(),
                "email": s.applicant.email,
                "role": s.applicant.role,
            },
            "assessment": {"id": s.assessment_id,
                           "title": s.assessment.title if s.assessment else "Assessment"},
            "percentage": float(s.percentage or 0),
            "score": float(s.score or 0),
            "completed_at": s.completed_at,
            "ai_summary": s.ai_summary,
        } for s in sessions],
        "pagination": {"total": total, "page": page, "limit": limit,
                       "pages": (total + limit - 1) // limit if total else 0},
    }


async def approve_applicant(
    db: AsyncSession,
    session_id: str,
    approve: bool = True,
    notes: str = None,
) -> dict:
    """
    Approve (or decline) a passed applicant. On approval the user becomes a
    developer, gets fresh credentials, and an email with results + login.
    """
    session = await db.scalar(
        select(AssessmentSession)
        .options(selectinload(AssessmentSession.applicant),
                 selectinload(AssessmentSession.assessment))
        .where(AssessmentSession.id == session_id)
    )
    if not session:
        raise ValueError("Assessment session not found")
    if session.status != "completed":
        raise ValueError("Session is not completed")
    if session.onboarding_status != "pending":
        raise ValueError("A decision has already been made for this session")

    session.onboarding_status = "approved" if approve else "declined"
    session.onboarding_decided_at = datetime.now()
    session.onboarding_notes = notes

    if not approve:
        await db.commit()
        return {"message": "Application declined", "session_id": session_id}

    user = session.applicant
    if not user:
        raise ValueError("Applicant account not found")

    temp_password = generate_temporary_password()
    user.password_hash = get_password_hash(temp_password)
    user.role = "developer"
    user.is_active = True
    await db.commit()

    name = f"{user.first_name} {user.last_name}".strip() or "there"
    html = onboarding_email_html(
        applicant_name=name,
        assessment_title=session.assessment.title if session.assessment else "Assessment",
        percentage=float(session.percentage or 0),
        login_email=user.email,
        temp_password=temp_password,
    )
    await send_email(
        user.email,
        "N.O.U Digital Systems - You're approved! Your developer login",
        html,
    )
    logger.info("onboarding: approved session %s -> developer %s", session_id, user.email)

    payload = {
        "message": "Applicant approved and promoted to developer. "
                   "Results + new login credentials emailed.",
        "session_id": session_id,
        "developer": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        },
    }
    # Only surface the generated password in development (the email is the
    # real channel; leaking it in production responses would be a risk).
    if settings.ENVIRONMENT.lower() == "development":
        payload["developer"]["temp_password"] = temp_password
    return payload
