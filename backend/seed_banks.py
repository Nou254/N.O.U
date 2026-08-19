"""
Seed the question_bank table with 100 authored questions per professional
category (20 common + 20 category + 20 position + 20 practical + 20
professional), WITHOUT calling Groq. The questions were authored directly
and stored in bank_shared.py (common + professional templates) and
bank_data_1..7.py (category / position / practical per category).

Idempotent: existing questions for a category are removed and replaced, so
partial Groq banks (e.g. Business & Systems Analysis 10/100) are cleaned up.
Run:  python seed_banks.py
"""

import asyncio
import sys

from sqlalchemy import delete, select

from app.core.database import async_session_factory
from app.core.assessment_framework import PARTS, BANK_QUESTIONS_PER_PART
from app.models.personnel import PersonnelCategory
from app.models.project_release import ProjectRelease  # noqa: F401  (mapper)
from app.models.question_bank import QuestionBankQuestion

import bank_shared
import bank_data_1
import bank_data_2
import bank_data_3
import bank_data_4
import bank_data_5
import bank_data_6
import bank_data_7

# Allowed question types per part (from assessment_framework).
ALLOWED_TYPES = {
    "common": {"scenario", "written_explanation", "debugging"},
    "category": {"written_explanation", "scenario", "design", "short_answer"},
    "position": {"written_explanation", "scenario", "debugging", "short_answer", "design"},
    "practical": {"practical", "design", "project", "debugging"},
    "professional": {"scenario", "written_explanation"},
}

DATA_FILES = [
    bank_data_1, bank_data_2, bank_data_3, bank_data_4,
    bank_data_5, bank_data_6, bank_data_7,
]


def build_question_sets() -> dict:
    """name -> {part: [(type, text, notes), ...]} for all 5 parts."""
    sets: dict = {}
    for mod in DATA_FILES:
        for name, parts in mod.CATS.items():
            if name in sets:
                raise SystemExit(f"DUPLICATE category in data files: {name}")
            sets[name] = {
                "common": list(bank_shared.COMMON),
                "category": list(parts["category"]),
                "position": list(parts["position"]),
                "practical": list(parts["practical"]),
                "professional": list(bank_shared.PROFESSIONAL),
            }
    return sets


def validate_sets(sets: dict) -> None:
    errors = []
    for name, parts in sets.items():
        for part in PARTS:
            qs = parts.get(part, [])
            if len(qs) != BANK_QUESTIONS_PER_PART:
                errors.append(
                    f"{name} [{part}] has {len(qs)} questions, "
                    f"expected {BANK_QUESTIONS_PER_PART}"
                )
                continue
            for qtype, text, notes in qs:
                if qtype not in ALLOWED_TYPES[part]:
                    errors.append(
                        f"{name} [{part}] uses disallowed type '{qtype}' "
                        f"(allowed: {sorted(ALLOWED_TYPES[part])})"
                    )
                if not text or len(text) < 20:
                    errors.append(f"{name} [{part}] has a short/empty question")
    if errors:
        for e in errors[:40]:
            print("ERROR:", e)
        raise SystemExit(f"Validation failed with {len(errors)} error(s)")


async def run() -> None:
    sets = build_question_sets()
    validate_sets(sets)
    print(f"Validated {len(sets)} categories x 100 questions", flush=True)

    async with async_session_factory() as db:
        cats = (await db.execute(select(PersonnelCategory))).scalars().all()
        by_name = {c.name: c for c in cats}

        missing = [n for n in sets if n not in by_name]
        if missing:
            print("WARN: categories in data but not in DB:", missing)
        unknown = [c.name for c in cats if c.name not in sets and c.is_active == "active"]
        print("WARN: active DB categories without a seeded bank:", unknown)

        done = 0
        for name, parts in sets.items():
            cat = by_name.get(name)
            if cat is None:
                print(f"SKIP {name}: not in DB", flush=True)
                continue

            # Remove any existing questions (partial Groq banks etc.).
            await db.execute(
                delete(QuestionBankQuestion).where(
                    QuestionBankQuestion.category_id == cat.id
                )
            )
            inserted = 0
            for part in PARTS:
                for qtype, text, notes in parts[part]:
                    db.add(QuestionBankQuestion(
                        category_id=cat.id,
                        category_name=name,
                        part=part,
                        question_type=qtype,
                        question_text=text,
                        grading_notes=notes,
                        points=10,
                        is_active=True,
                    ))
                    inserted += 1
            await db.commit()
            done += 1
            print(f"OK  {name}: {inserted} questions", flush=True)

        print(f"DONE: {done} categories seeded", flush=True)


if __name__ == "__main__":
    asyncio.run(run())
