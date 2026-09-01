"""
Generate the 100-question AI bank for every professional category that is
not ready yet. Resumable (ready categories are skipped, partial banks are
topped up) and shardable so multiple processes can run in parallel.

Usage:
    python generate_banks.py                   # generate everything (sequential)
    python generate_banks.py 0 0 3             # shard 0 of 3 (stagger 0s)
    python generate_banks.py 20 1 3 4          # shard 1 of 3, at most 4 categories

Each category takes ~2-4 minutes (100 questions via Groq, 10 batches).
"""

import asyncio
import sys
import time

from sqlalchemy import select

from app.core.database import async_session_factory
# Register models referenced lazily by the mapper (same set as app.main).
from app.models.project_release import ProjectRelease  # noqa: F401
from app.models.question_bank import QuestionBankQuestion  # noqa: F401
from app.models.personnel import PersonnelCategory
from app.services.question_bank import ensure_bank, bank_counts
from app.core.assessment_framework import PARTS, BANK_QUESTIONS_PER_PART

TARGET = BANK_QUESTIONS_PER_PART * len(PARTS)  # 20 x 5 = 100


async def main() -> None:
    stagger = float(sys.argv[1]) if len(sys.argv) > 1 else 0
    shard = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    shards = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    max_count = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9

    if stagger:
        print(f"[shard {shard}] staggering {stagger:.0f}s", flush=True)
        await asyncio.sleep(stagger)

    # ---- Fetch category IDs and names as plain values ----
    async with async_session_factory() as db:
        result = await db.execute(
            select(PersonnelCategory.id, PersonnelCategory.name)
            .where(PersonnelCategory.is_active == "active")
            .order_by(PersonnelCategory.name)
        )
        categories = result.all()  # list of (id, name)

    # ---- Determine which categories need banks ----
    todo = []
    for cat_id, cat_name in categories:
        # Use a fresh session just to check counts
        async with async_session_factory() as check_db:
            counts = await bank_counts(check_db, cat_id)
            if sum(counts.values()) < TARGET:
                todo.append((cat_id, cat_name))

    mine = (todo[shard::shards] if shards > 1 else todo)[:max_count]
    print(f"[shard {shard}] {len(todo)} categories need banks; this shard has {len(mine)}", flush=True)

    ok = 0
    for cat_id, cat_name in mine:
        t0 = time.time()
        done = False
        # Retry once per category: a daily-token-quota failure exhausts one
        # key, and the pool then rotates to a fresh key for the retry.
        for attempt in range(1, 3):
            try:
                # ---- Use a fresh session for this category ----
                async with async_session_factory() as db:
                    # Fetch the category object fresh
                    cat = await db.get(PersonnelCategory, cat_id)
                    if cat is None:
                        print(
                            f"[shard {shard}] ERR {cat_name}: category not found",
                            flush=True,
                        )
                        break
                    counts = await ensure_bank(
                        db, cat, questions_per_part=BANK_QUESTIONS_PER_PART
                    )
                    total = sum(counts.values())
                    ok += 1
                    done = True
                    retry_note = " (retry)" if attempt > 1 else ""
                    print(
                        f"[shard {shard}] OK  {cat_name}: {total}/{TARGET} "
                        f"({time.time() - t0:.0f}s){retry_note}",
                        flush=True,
                    )
                    break
            except Exception as exc:  # noqa: BLE001 - report and continue
                if attempt < 2:
                    print(
                        f"[shard {shard}] retry {cat_name} after "
                        f"{type(exc).__name__} (key rotation)",
                        flush=True,
                    )
                else:
                    print(
                        f"[shard {shard}] ERR {cat_name}: {type(exc).__name__}: "
                        f"{str(exc)[:140]}",
                        flush=True,
                    )
        if not done:
            print(
                f"[shard {shard}] WARN {cat_name}: failed both attempts - "
                "will be picked up by a later run",
                flush=True,
            )

    print(f"[shard {shard}] DONE ({ok}/{len(mine)} ok)", flush=True)


if __name__ == "__main__":
    asyncio.run(main())