"""
Complaints API.

The public Complaints screen lets any visitor / customer / applicant file a
complaint. Every submission is stored and forwarded to the administration
(they review it on the admin Complaints screen). No login required - the
complainant only provides contact details so the admin can follow up.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import check_rate_limit
from app.core.security import get_optional_user
from app.models.user import User
from app.models.complaint import Complaint

router = APIRouter()


class ComplaintIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(default="", max_length=30)
    subject: str = Field(min_length=3, max_length=255)
    category: str = Field(default="General", max_length=60)
    message: str = Field(min_length=10, max_length=5000)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def submit_complaint(
    body: ComplaintIn,
    request: Request,
    current_user: User | None = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """File a complaint. No login required - it is forwarded to the admin."""
    check_rate_limit(request, "complaint:ip", max_hits=5, window_seconds=3600)

    complaint = Complaint(
        full_name=body.full_name.strip(),
        email=body.email.lower().strip(),
        phone=body.phone.strip() or None,
        subject=body.subject.strip(),
        category=body.category.strip() or "General",
        message=body.message.strip(),
        status="new",
    )
    db.add(complaint)
    await db.commit()
    await db.refresh(complaint)

    return {
        "message": (
            "Your complaint has been received and forwarded to our "
            "administration. We will review it and respond to you at "
            f"{complaint.email}."
        ),
        "complaint": {
            "id": complaint.id,
            "subject": complaint.subject,
            "status": complaint.status,
            "created_at": complaint.created_at,
        },
    }
