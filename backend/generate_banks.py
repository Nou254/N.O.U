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

    async with async_session_factory() as db:
        cats = (
            await db.execute(
                select(PersonnelCategory)
                .where(PersonnelCategory.is_active == "active")
                .order_by(PersonnelCategory.name)
            )
        ).scalars().all()

        todo = []
        for c in cats:
            counts = await bank_counts(db, c.id)
            if sum(counts.values()) < TARGET:
                todo.append(c)

        mine = (todo[shard::shards] if shards > 1 else todo)[:max_count]
        print(f"[shard {shard}] {len(todo)} categories need banks; this shard has {len(mine)}", flush=True)

        ok = 0
        for cat in mine:
            # Snapshot plain values BEFORE any transaction: rollbacks and
            # commits expire ORM attributes, and reloading them in async
            # context crashes (MissingGreenlet).
            cat_id = cat.id
            cat_name = cat.name
            t0 = time.time()
            done = False
            # Retry once per category: a daily-token-quota failure exhausts one
            # key, and the pool then rotates to a fresh key for the retry.
            for attempt in range(1, 3):
                try:
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
                    try:
                        await db.rollback()
                    except Exception:  # noqa: BLE001
                        pass
                    if attempt < 2:
                        # The rollback expired the category object - fetch a
                        # fresh one so the retry works with a live instance.
                        try:
                            cat = await db.get(PersonnelCategory, cat_id)
                        except Exception:  # noqa: BLE001
                            pass
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
