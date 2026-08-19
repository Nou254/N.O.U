"""
Background worker that emails assessment results to applicants 2 hours after
submission (product rule). A lightweight asyncio loop polls for completed
sessions that have not yet had their results emailed and whose completed_at
is at least RESULTS_EMAIL_DELAY_HOURS in the past.

The worker is started from the FastAPI lifespan (app/main.py). For a
multi-worker production deployment prefer a real scheduler/queue; this is
correct for the single-worker development deployment.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta

from sqlalchemy import select

from app.core.assessment_framework import QUALIFYING_PERCENT
from app.core.assessment_modules import (
    COMPULSORY_MODULES,
    RESULTS_EMAIL_DELAY_HOURS,
)
from app.core.database import async_session_factory
from app.models.assessment import (
    AssessmentSession,
    AssessmentAnswer,
    AssessmentSessionQuestion,
)
from app.models.assessment import Assessment
from app.models.user import User
from app.services.email import send_email, results_email_html

logger = logging.getLogger("results_email")

POLL_INTERVAL_SECONDS = 60


def _module_breakdown(session: AssessmentSession, answers: list, questions: list) -> list:
    """Recompute per-module percentages from stored answers + questions."""
    totals: dict = {}
    for sq in questions:
        entry = totals.setdefault(sq.module, {"score": 0.0, "max": 0.0})
        entry["max"] += sq.points
        answer = next((a for a in answers if a.session_question_id == sq.id), None)
        if answer:
            entry["score"] += answer.points_earned or 0

    return [
        {
            "module": module,
            "percentage": (e["score"] / e["max"] * 100) if e["max"] else 0,
            "compulsory": module in COMPULSORY_MODULES,
        }
        for module, e in totals.items()
    ]


async def _send_one(session: AssessmentSession) -> None:
    async with async_session_factory() as db:
        # Reload relationships within this session.
        session = await db.get(AssessmentSession, session.id)
        applicant = await db.get(User, session.applicant_id)
        assessment = await db.get(Assessment, session.assessment_id)

        answers_result = await db.execute(
            select(AssessmentAnswer).where(AssessmentAnswer.session_id == session.id)
        )
        answers = answers_result.scalars().all()

        questions_result = await db.execute(
            select(AssessmentSessionQuestion)
            .where(AssessmentSessionQuestion.session_id == session.id)
        )
        questions = questions_result.scalars().all()

        breakdown = _module_breakdown(session, answers, questions)
        percentage = float(session.percentage or 0)
        passed = (session.ai_recommendation or "").upper() == "PASS"

        if not applicant or not applicant.email:
            logger.warning("session %s has no applicant email; skipping", session.id)
            return

        name = f"{applicant.first_name} {applicant.last_name}".strip() or "there"

        # The results email ALWAYS goes out alone - it never contains login
        # credentials. Credentials are only issued later by the administration
        # when a passed applicant is approved (onboarding.approve_applicant),
        # per the recruitment rule: results first, admin approval, then
        # credentials.
        login_email = ""
        temp_password = ""

        # FAIL -> build the reason(s) for failure from the score, the weak
        # sections, the AI summary and the recommended alternative category.
        failure_reasons = None
        if not passed:
            failure_reasons = [
                f"Overall score of {percentage:.1f}% was below the {QUALIFYING_PERCENT}% qualifying mark."
            ]
            weak = [
                m["module"]
                for m in breakdown
                if m.get("percentage", 0) < 50
            ]
            if weak:
                failure_reasons.append(
                    "Scores were below 50% in: " + ", ".join(weak) + "."
                )
            if session.ai_summary:
                failure_reasons.append("AI summary: " + session.ai_summary[:400])
            if session.recommended_category:
                failure_reasons.append(
                    "Recommended alternative career: " + session.recommended_category + "."
                )

        html = results_email_html(
            applicant_name=name,
            assessment_title=assessment.title if assessment else "Assessment",
            percentage=percentage,
            passed=passed,
            module_breakdown=breakdown,
            login_email="",
            temp_password="",
            failure_reasons=failure_reasons,
        )
        await send_email(
            applicant.email,
            f"N.O.U Assessment Result - {assessment.title if assessment else 'Assessment'}",
            html,
        )
        session.results_emailed_at = datetime.now()
        await db.commit()
        logger.info(
            "results emailed for session %s to %s (%.1f%%)",
            session.id, applicant.email, percentage,
        )


async def _send_pending() -> int:
    # Local time to match MySQL func.now()/completed_at convention.
    cutoff = datetime.now() - timedelta(hours=RESULTS_EMAIL_DELAY_HOURS)
    async with async_session_factory() as db:
        result = await db.execute(
            select(AssessmentSession).where(
                AssessmentSession.status == "completed",
                AssessmentSession.results_emailed_at.is_(None),
                AssessmentSession.completed_at <= cutoff,
            )
        )
        sessions = result.scalars().all()
    for session in sessions:
        try:
            await _send_one(session)
        except Exception as exc:  # noqa: BLE001
            logger.exception("failed to email results for session %s: %s", session.id, exc)
    return len(sessions)


async def results_email_worker() -> None:
    """Background loop: email results for sessions past the 2-hour mark."""
    logger.info("results-email worker started (delay: %sh)", RESULTS_EMAIL_DELAY_HOURS)
    while True:
        try:
            sent = await _send_pending()
            if sent:
                logger.info("results-email worker sent %d result email(s)", sent)
        except asyncio.CancelledError:
            logger.info("results-email worker cancelled")
            raise
        except Exception as exc:  # noqa: BLE001
            logger.exception("results-email worker error: %s", exc)
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
