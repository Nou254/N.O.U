"""
Shared helpers for assembling AI assessment result payloads.

Used by both the applicant-facing results endpoint (assessments.py) and the
admin review endpoints (admin.py) so the per-question feedback shape stays
in one place.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assessment import AssessmentAnswer, AssessmentSessionQuestion


async def build_session_feedback(db: AsyncSession, session_id: str) -> list:
    """
    Build the per-question AI feedback list for a completed session.

    Each item contains: question, category, points, user_answer, score,
    max_score, and the AI feedback. AI-generated questions live in
    assessment_session_questions; their grades are in assessment_answers.
    """
    answers_result = await db.execute(
        select(AssessmentAnswer).where(AssessmentAnswer.session_id == session_id)
    )
    answers = answers_result.scalars().all()

    sq_result = await db.execute(
        select(AssessmentSessionQuestion)
        .where(AssessmentSessionQuestion.session_id == session_id)
        .order_by(AssessmentSessionQuestion.order_number)
    )
    session_questions = sq_result.scalars().all()

    feedback = []
    for sq in session_questions:
        answer = next((a for a in answers if a.session_question_id == sq.id), None)
        feedback.append({
            "question": sq.question_text,
            "module": sq.module,
            "category": sq.category,
            "points": sq.points,
            "user_answer": answer.user_answer if answer else None,
            "score": answer.points_earned if answer else 0,
            "max_score": sq.points,
            "feedback": answer.ai_feedback if answer else None,
        })

    return feedback
