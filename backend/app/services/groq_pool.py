"""
Groq API key pool.

Manages a pool of up to 60 Groq API keys (configured as a comma-separated
list in GROQ_API_KEYS in backend/.env) shared across every AI feature:

- **Sections** (each with its own daily key budget): ``assessments``
  (question generation + grading), ``nou_lite`` (customer AI assistant),
  ``project_chat`` (project chat AI help).
- Each section gets **GROQ_KEYS_PER_SECTION (10) keys per day**, allocated
  from the pool round-robin.
- When a section exhausts its 10 keys for the day, it is topped up with
  **GROQ_KEYS_TOP_UP (2) more keys**.
- Keys that fail authentication/expiry (401) are marked failed and skipped
  for the rest of the day (rotation to the next healthy key happens
  automatically on the next call).

Usage is persisted in the ``ai_key_usage`` table so budget state survives
server restarts. All pool state is guarded by a lock (single worker is fine;
the table keeps multi-worker restarts consistent).
"""

import logging
import threading
from datetime import date
from typing import List, Optional

from groq import AsyncGroq

from app.core.config import settings
from app.core.database import async_session_factory
from app.models.ai_key_usage import AIKeyUsage

logger = logging.getLogger("groq_pool")

# AI sections and their display labels.
SECTIONS = ("assessments", "nou_lite", "project_chat")

# Each AI section draws its daily key budget from a dedicated key pool
# (groq_apis.md was split into backend/.env accordingly):
#   assessments  -> GROQ_ASSESSMENT_KEYS (question generation + grading)
#   nou_lite     -> GROQ_CHATBOT_KEYS    (N.O.U Lite customer assistant)
#   project_chat -> GROQ_COMMUNITY_KEYS  (project chat / community AI)
SECTION_KEY_ENVS = {
    "assessments": "GROQ_ASSESSMENT_KEYS",
    "nou_lite": "GROQ_CHATBOT_KEYS",
    "project_chat": "GROQ_COMMUNITY_KEYS",
}

_lock = threading.Lock()
# section -> list of key indices usable today (allocated + topped up)
_active: dict = {}
# section -> round-robin cursor
_cursor: dict = {}
# section -> set of key indices that failed today (401/expired)
_failed: dict = {}


def _all_keys(section: str = None) -> List[str]:
    """Return the configured key list for a section's dedicated pool,
    falling back to the shared GROQ_API_KEYS / GROQ_API_KEY."""
    keys: List[str] = []
    env_name = SECTION_KEY_ENVS.get(section) if section else None
    if env_name:
        keys = list(getattr(settings, env_name, []) or [])
    if not keys:
        keys = list(settings.GROQ_API_KEYS or [])
    if settings.GROQ_API_KEY and settings.GROQ_API_KEY not in keys:
        keys.insert(0, settings.GROQ_API_KEY)
    return keys


async def _load_daily_state() -> None:
    """Load today's usage from the DB into memory (called once per day)."""
    today = date.today()
    _active.clear()
    _cursor.clear()
    _failed.clear()
    async with async_session_factory() as db:
        from sqlalchemy import select
        rows = (await db.execute(
            select(AIKeyUsage).where(AIKeyUsage.usage_date == today)
        )).scalars().all()
    by_section: dict = {}
    for row in rows:
        by_section.setdefault(row.section, []).append(row)
    for section in SECTIONS:
        used = sorted({r.key_index for r in by_section.get(section, [])})
        _failed.setdefault(section, set()).update(
            r.key_index for r in by_section.get(section, []) if r.failed
        )
        total_keys = len(_all_keys(section))
        _active[section] = used if used else list(range(min(total_keys, settings.GROQ_KEYS_PER_SECTION)))
        _cursor[section] = 0


_loaded_day: Optional[date] = None


async def _ensure_loaded() -> None:
    global _loaded_day
    today = date.today()
    if _loaded_day != today:
        await _load_daily_state()
        _loaded_day = today


async def _persist(section: str, key_index: int, failed: bool = False) -> None:
    today = date.today()
    async with async_session_factory() as db:
        from sqlalchemy import select
        row = (await db.execute(
            select(AIKeyUsage).where(
                AIKeyUsage.usage_date == today,
                AIKeyUsage.section == section,
                AIKeyUsage.key_index == key_index,
            )
        )).scalar_one_or_none()
        if row is None:
            row = AIKeyUsage(usage_date=today, section=section, key_index=key_index,
                             requests=0)
            db.add(row)
        row.requests = (row.requests or 0) + 1
        if failed:
            row.failed = True
        await db.commit()


async def _top_up(section: str) -> None:
    """Give a section GROQ_KEYS_TOP_UP more keys after it exhausted its budget."""
    total = len(_all_keys(section))
    allocated = set(_active.get(section, []))
    available = [i for i in range(total) if i not in allocated]
    added = 0
    for idx in available:
        if added >= settings.GROQ_KEYS_TOP_UP:
            break
        _active.setdefault(section, []).append(idx)
        added += 1
    if added:
        logger.info("groq_pool: topped up section %s with %d key(s)", section, added)


def _next_key_index(section: str) -> Optional[int]:
    """Pick the next healthy key index for a section (round-robin, skip failed)."""
    pool = _active.get(section, [])
    if not pool:
        return None
    failed = _failed.setdefault(section, set())
    cursor = _cursor.get(section, 0)
    for _ in range(len(pool)):
        idx = pool[cursor % len(pool)]
        cursor += 1
        if idx not in failed:
            _cursor[section] = cursor
            return idx
    return None


def _key_value(section: str, index: int) -> str:
    keys = _all_keys(section)
    return keys[index] if 0 <= index < len(keys) else settings.GROQ_API_KEY or ""


def mark_failed(section: str, key_index: Optional[int]) -> None:
    """Mark a key as failed for the rest of the day (401 / token expired)."""
    if key_index is None:
        return
    with _lock:
        _failed.setdefault(section, set()).add(key_index)
    logger.warning("groq_pool: marked key#%s failed for section %s", key_index, section)


def pool_status() -> dict:
    """Snapshot of the pool for admin/debug endpoints."""
    return {
        "sections": {
            s: {"total_keys": len(_all_keys(s)), "keys": [f"...{k[-4:]}" for k in _all_keys(s)]}
            for s in SECTIONS
        },
        "active": {s: list(v) for s, v in _active.items()},
        "failed": {s: sorted(v) for s, v in _failed.items()},
        "cursor": dict(_cursor),
    }


async def get_client(section: str) -> tuple:
    """
    Return (AsyncGroq client, key_index) for the given section, allocating
    from that section's daily key budget. Raises RuntimeError when no healthy
    key is available (callers map it to a 503).
    """
    if section not in SECTIONS:
        raise ValueError(f"unknown AI section: {section}")
    if not _all_keys(section):
        raise RuntimeError(
            "The AI engine is not configured: set GROQ_API_KEY (or the "
            "per-section GROQ_ASSESSMENT_KEYS / GROQ_CHATBOT_KEYS / "
            "GROQ_COMMUNITY_KEYS) in backend/.env and restart."
        )

    await _ensure_loaded()

    # Synchronous in-memory allocation (fast, no awaits inside the lock).
    with _lock:
        idx = _next_key_index(section)
        if idx is None:
            # Section exhausted its daily keys -> top up and retry once.
            await _top_up(section)
            idx = _next_key_index(section)
        if idx is None:
            raise RuntimeError(
                f"The {section} AI section has no healthy API keys left for "
                "today. Please try again tomorrow (or add more GROQ_API_KEYS)."
            )

    # Persist usage outside the lock (DB I/O must not block the event loop).
    await _persist(section, idx)
    return AsyncGroq(api_key=_key_value(section, idx), timeout=settings.GROQ_TIMEOUT), idx
