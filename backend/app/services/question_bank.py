"""
Question bank service.

The question bank holds 100 pre-generated AI questions per professional
category (20 per assessment part). Assessments draw 20 random questions from
it, so exam starts are instant and Groq is never called mid-exam.

- ensure_bank()  - top-up the category's bank to the target size (generating
                   missing questions with Groq, committing after every batch
                   so partial progress survives failures/restarts).
- pick_questions() - select the per-part random set for one assessment.
"""

import asyncio
import logging
from typing import Dict, List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.assessment_framework import (
    PARTS,
    PART_QUESTION_TYPES,
    QUESTIONS_PER_PART,
    BANK_QUESTIONS_PER_PART,
    BANK_SIZE_PER_CATEGORY,
)
from app.models.personnel import PersonnelCategory
from app.models.question_bank import QuestionBankQuestion
from app.services import ai_assessment

logger = logging.getLogger("question_bank")

# Per-process locks so concurrent applicants (or admin + applicant) never
# generate the same category's bank twice at the same time.
_BANK_LOCKS: Dict[int, asyncio.Lock] = {}


def _bank_lock(category_id: int) -> asyncio.Lock:
    return _BANK_LOCKS.setdefault(category_id, asyncio.Lock())


def _part_specs(category: PersonnelCategory) -> List[dict]:
    """The 5 assessment parts with labels/types/focus for the generator."""
    return [
        {
            "part": "common",
            "label": "Common Assessment",
            "types": PART_QUESTION_TYPES["common"],
            "focus": (
                "logic, critical thinking and general computer / professional "
                "knowledge - real-world problems, not puzzles"
            ),
        },
        {
            "part": "category",
            "label": "Category Assessment",
            "types": PART_QUESTION_TYPES["category"],
            "focus": f"knowledge of the {category.name} professional field",
        },
        {
            "part": "position",
            "label": "Position Assessment",
            "types": PART_QUESTION_TYPES["position"],
            "focus": (
                "knowledge a professional in this field applies on the job - "
                "role-level scenarios, tools, practices and decision-making"
            ),
        },
        {
            "part": "practical",
            "label": "Practical Assessment",
            "types": PART_QUESTION_TYPES["practical"],
            "focus": "the ability to perform an actual task - design, build or troubleshoot",
        },
        {
            "part": "professional",
            "label": "Professional Assessment",
            "types": PART_QUESTION_TYPES["professional"],
            "focus": "communication, ethics, teamwork and professional judgement",
        },
    ]


async def bank_counts(db: AsyncSession, category_id: int) -> Dict[str, int]:
    """Return the number of active bank questions per part for a category."""
    rows = await db.execute(
        select(
            QuestionBankQuestion.part,
            func.count(QuestionBankQuestion.id),
        )
        .where(
            QuestionBankQuestion.category_id == category_id,
            QuestionBankQuestion.is_active == True,  # noqa: E712
        )
        .group_by(QuestionBankQuestion.part)
    )
    return {part: int(count) for part, count in rows.all()}


async def ensure_bank(
    db: AsyncSession,
    category: PersonnelCategory,
    questions_per_part: int = BANK_QUESTIONS_PER_PART,
) -> Dict[str, int]:
    """
    Make sure the category's question bank holds ``questions_per_part`` active
    questions per part (default 20 x 5 = 100 per category). Only the missing
    questions are generated, in chunks of 10 with a commit after EVERY chunk,
    so a failure mid-way keeps what was already produced and the next call
    tops up. Idempotent and safe to re-run.
    """
    async with _bank_lock(category.id):
        counts = await bank_counts(db, category.id)
        missing_parts = [p for p in PARTS if counts.get(p, 0) < questions_per_part]
        if not missing_parts:
            return counts

        total_generated = 0
        for part in missing_parts:
            needed = questions_per_part - counts.get(part, 0)
            if needed <= 0:
                continue
            spec = next(
                (s for s in _part_specs(category) if s["part"] == part),
                None,
            )
            parts = [spec] if spec else [{"part": part, "label": part.capitalize()}]
            # Generate in chunks of 10 and commit after every chunk so a
            # failure mid-way keeps the questions already produced.
            while needed > 0:
                take = min(needed, ai_assessment.BANK_BATCH_SIZE)
                try:
                    generated = await ai_assessment.generate_question_bank(
                        category_name=category.name,
                        assessment_title=f"N.O.U {category.name} Assessment",
                        assessment_description=category.description,
                        questions_per_part=take,
                        parts=parts,
                    )
                except (ai_assessment.AINotConfiguredError, ai_assessment.AIAPIError):
                    # A partial bank is still useful - surface the error so
                    # the caller can decide (applicant sees a retryable msg).
                    raise

                for q in generated:
                    db.add(QuestionBankQuestion(
                        category_id=category.id,
                        category_name=category.name,
                        part=part,
                        question_type=q.get("question_type", "written_explanation"),
                        question_text=q["question_text"],
                        grading_notes=q.get("grading_notes", ""),
                        points=q.get("points", 10) or 10,
                    ))
                await db.commit()
                total_generated += len(generated)
                needed -= take
                logger.info(
                    "Bank: generated %d %s questions for category %s (part=%s)",
                    len(generated), category.name, category.id, part,
                )

        return await bank_counts(db, category.id)


async def pick_questions(
    db: AsyncSession,
    category_id: int,
    per_part: Optional[Dict[str, int]] = None,
) -> List[QuestionBankQuestion]:
    """
    Select the randomized question set for one assessment from the category's
    bank: ``per_part`` questions per assessment part (defaults to the 20-question
    framework). Selection is random within each part (ORDER BY RAND() - MySQL);
    if a part is short, the deficit is topped up from the rest of the bank.
    The returned list keeps framework part order (common -> professional).
    """
    per_part = per_part or dict(QUESTIONS_PER_PART)
    picked: List[QuestionBankQuestion] = []
    used_ids: set = set()

    for part in PARTS:
        want = max(0, int(per_part.get(part, 0)))
        if want <= 0:
            continue
        rows = (
            await db.execute(
                select(QuestionBankQuestion)
                .where(
                    QuestionBankQuestion.category_id == category_id,
                    QuestionBankQuestion.part == part,
                    QuestionBankQuestion.is_active == True,  # noqa: E712
                )
                .order_by(func.rand())
                .limit(want)
            )
        ).scalars().all()
        for q in rows:
            picked.append(q)
            used_ids.add(q.id)

    # Top-up shortfalls (e.g. a part with fewer bank questions than needed)
    # from the remaining bank across all parts - still random.
    shortfall = sum(
        max(0, int(per_part.get(p, 0))) for p in PARTS
    ) - len(picked)
    if shortfall > 0:
        rows = (
            await db.execute(
                select(QuestionBankQuestion)
                .where(
                    QuestionBankQuestion.category_id == category_id,
                    QuestionBankQuestion.is_active == True,  # noqa: E712
                    QuestionBankQuestion.id.notin_(list(used_ids)) if used_ids
                    else QuestionBankQuestion.id.isnot(None),
                )
                .order_by(func.rand())
                .limit(shortfall)
            )
        ).scalars().all()
        picked.extend(rows)

    return picked
