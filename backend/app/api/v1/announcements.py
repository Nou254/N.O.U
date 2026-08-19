"""
Announcements API (the "quorum" communications space).

- Admins post jokes of the day, quotes, notices, or any communication aimed
  at developers and/or customers.
- Developers and customers read their role-scoped feed on their dashboards.
- Admins can broadcast an email to all customers (maintenance windows,
  incoming services, etc.) using the transactional email service.
"""

import asyncio

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.core.security import require_admin, require_authenticated
from app.models.user import User
from app.models.announcement import Announcement
from app.services.email import send_email, announcement_email_html

router = APIRouter()

AUDIENCES = {"all", "developers", "customers"}
CATEGORIES = {"joke", "quote", "notice", "update"}


def _announcement_payload(a: Announcement) -> dict:
    return {
        "id": a.id,
        "title": a.title,
        "body": a.body,
        "category": a.category,
        "audience": a.audience,
        "pinned": a.pinned,
        "created_by": a.created_by,
        "created_at": a.created_at,
    }


# ---------------------------------------------------------------------------
# Admin management
# ---------------------------------------------------------------------------
class AnnouncementIn(BaseModel):
    body: str = Field(..., min_length=1, max_length=5000)
    title: Optional[str] = Field(None, max_length=255)
    category: str = Field("update", pattern="^(joke|quote|notice|update)$")
    audience: str = Field("all", pattern="^(all|developers|customers)$")
    pinned: bool = False


@router.post("/announcements", status_code=status.HTTP_201_CREATED)
async def create_announcement(
    body: AnnouncementIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Admins post an announcement (joke of the day, quote, notice, update)."""
    announcement = Announcement(
        body=body.body,
        title=body.title,
        category=body.category,
        audience=body.audience,
        pinned=body.pinned,
        created_by=current_user.id,
    )
    db.add(announcement)
    await db.commit()
    await db.refresh(announcement)
    return _announcement_payload(announcement)


@router.get("/announcements")
async def admin_list_announcements(
    audience: Optional[str] = Query(None),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Admins list every announcement, newest first."""
    query = select(Announcement)
    if audience:
        query = query.where(Announcement.audience.in_([audience, "all"]))
    result = await db.execute(
        query.order_by(Announcement.pinned.desc(),
                       Announcement.created_at.desc())
    )
    return {"announcements": [_announcement_payload(a) for a in result.scalars().all()]}


@router.delete("/announcements/{announcement_id}")
async def delete_announcement(
    announcement_id: str,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Admins remove an announcement."""
    announcement = await db.scalar(
        select(Announcement).where(Announcement.id == announcement_id)
    )
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    await db.delete(announcement)
    await db.commit()
    return {"message": "Announcement deleted"}


class EmailBroadcastIn(BaseModel):
    subject: str = Field(..., min_length=3, max_length=200)
    body: str = Field(..., min_length=10, max_length=10000)


@router.post("/announcements/email")
async def email_broadcast(
    payload: EmailBroadcastIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Batch-email all customers (e.g. maintenance windows, incoming services).
    Emails are delivered concurrently (bounded pool) through the configured
    SMTP service; if SMTP is not configured they go to the dev email log.
    """
    result = await db.execute(
        select(User).where(User.role == "customer", User.is_active == True)  # noqa: E712
    )
    customers = result.scalars().all()
    if not customers:
        return {
            "message": "No customers to notify",
            "emailed": 0,
        }

    semaphore = asyncio.Semaphore(8)

    async def deliver(customer: User) -> bool:
        async with semaphore:
            try:
                await send_email(
                    customer.email,
                    payload.subject,
                    announcement_email_html(payload.body, payload.subject),
                )
                return True
            except Exception:  # noqa: BLE001 - one bad address must not stop the batch
                return False

    results_list = await asyncio.gather(*(deliver(c) for c in customers))
    delivered = sum(1 for ok in results_list if ok)
    failed = len(results_list) - delivered

    return {
        "message": f"Broadcast sent to {delivered} customer(s)",
        "emailed": delivered,
        "failed": failed,
    }


@router.get("/announcements/customers-count")
async def customers_count(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Number of customer email addresses for the broadcast form."""
    count = await db.scalar(
        select(func.count())
        .select_from(User)
        .where(User.role == "customer", User.is_active == True)  # noqa: E712
    )
    return {"customers": count or 0}


# ---------------------------------------------------------------------------
# Role-scoped feed (developers + customers)
# ---------------------------------------------------------------------------
@router.get("/announcements/feed")
async def announcement_feed(
    current_user: User = Depends(require_authenticated),
    db: AsyncSession = Depends(get_db),
):
    """
    Announcements for the logged-in user's role. Developers see announcements
    aimed at developers + all; customers see customer + all; admins see all.
    """
    if current_user.role == "developer":
        audiences = ["all", "developers"]
    elif current_user.role == "customer":
        audiences = ["all", "customers"]
    else:
        audiences = ["all", "developers", "customers"]

    result = await db.execute(
        select(Announcement)
        .where(Announcement.audience.in_(audiences))
        .order_by(Announcement.pinned.desc(),
                  Announcement.created_at.desc())
        .limit(50)
    )
    return {"announcements": [_announcement_payload(a) for a in result.scalars().all()]}
