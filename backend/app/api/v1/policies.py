"""
Organization policies router.

Serves the N.O.U. Organization Policies document (chapters 1-14 of the master
document). The document is stored in the site_policies table and seeded from
app/data/organization_policies.txt. It is shown:

- to approved personnel on their first login (they must agree before use),
- on every admin category screen after approval (for future reference).
"""

import logging
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_factory, get_db
from app.models.site_policy import SitePolicy

logger = logging.getLogger("policies")

router = APIRouter(tags=["Policies"])

# Location of the policies text file bundled with the backend. The admin can
# re-run the seed (or the backend re-seeds at startup if the table is empty).
POLICIES_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "organization_policies.txt"


async def ensure_policies_seeded() -> None:
    """
    Seed the site_policies table from the bundled text file if it is empty.
    Called at startup so a fresh database always has the document.
    """
    try:
        async with async_session_factory() as db:
            existing = await db.scalar(select(SitePolicy).order_by(SitePolicy.id).limit(1))
            if existing:
                return
            if not POLICIES_FILE.exists():
                logger.warning("policies file not found at %s", POLICIES_FILE)
                return
            content = POLICIES_FILE.read_text(encoding="utf-8")
            db.add(SitePolicy(
                title="N.O.U. Organization Policies",
                content=content,
                version="1.0",
            ))
            await db.commit()
            logger.info("Seeded organization policies (%d chars)", len(content))
    except Exception:  # noqa: BLE001 - seeding must never block startup
        logger.exception("Failed to seed organization policies")


@router.get("/")
async def get_policies(
    db: AsyncSession = Depends(get_db),
):
    """Return the latest organization policies document (public - it is the
    company's own policies and is shown to approved personnel for consent)."""
    policy = await db.scalar(select(SitePolicy).order_by(SitePolicy.id.desc()).limit(1))
    if not policy:
        # Fallback: serve from the bundled file so the consent page never
        # breaks even if the DB row was removed.
        if POLICIES_FILE.exists():
            return {
                "title": "N.O.U. Organization Policies",
                "content": POLICIES_FILE.read_text(encoding="utf-8"),
                "version": "1.0",
                "updated_at": None,
            }
        raise HTTPException(status_code=404, detail="Organization policies not available")
    return {
        "title": policy.title,
        "content": policy.content,
        "version": policy.version,
        "updated_at": policy.updated_at,
    }
