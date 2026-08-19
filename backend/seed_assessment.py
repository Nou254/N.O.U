"""
Seed the Employment Assessment record.

The assessment UI lists active assessments from the assessments table. This
script inserts the single N.O.U. Employment Assessment (AI-generated,
5-part framework) if it is missing. Idempotent.

Usage (from backend/):
    python seed_assessment.py
"""

import asyncio

from sqlalchemy import select

# Register the full model set so SQLAlchemy can resolve string-based
# relationships when mappers are configured in standalone scripts.
import app.models.project_release  # noqa: F401

from app.core.database import async_session_factory
from app.models.assessment import Assessment

TITLE = "N.O.U. Employment Assessment"
DESCRIPTION = (
    "A five-part, AI-generated employment assessment tailored to your chosen "
    "professional category and position. Written answers only - no multiple "
    "choice. Qualifying score: 80%."
)


async def seed() -> None:
    async with async_session_factory() as db:
        existing = await db.scalar(
            select(Assessment).where(Assessment.title == TITLE)
        )
        if existing:
            print("Assessment already exists (id=%s)" % existing.id)
            return

        assessment = Assessment(
            title=TITLE,
            description=DESCRIPTION,
            duration_minutes=210,   # 3 hours 30 minutes (framework default)
            total_questions=29,     # 8+8+8+3+2 across the five parts
            passing_score=80,       # N.O.U. Qualified threshold
            is_active=True,
        )
        db.add(assessment)
        await db.commit()
        print("Created assessment: %s (id=%s)" % (TITLE, assessment.id))


if __name__ == "__main__":
    asyncio.run(seed())
