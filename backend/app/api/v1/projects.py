"""
Project request API endpoints (customer side).

Implements the customer portion of the N.O.U. quotation workflow
(today.md docs 8 + 9): request registration with a unique number, quotation
acceptance/declining, and deposit payment submission. Admin-side review,
feasibility, quotation and payment verification live in admin.py.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime

from app.core.database import get_db
from app.core.rate_limit import check_rate_limit
from app.core.security import (
    require_customer, ensure_customer_profile, get_password_hash,
)
from app.models.user import User
from app.models.customer import Customer
from app.models.project_request import ProjectRequest, ProjectPayment

router = APIRouter()

VALID_STATUSES = {
    "submitted", "under_review", "clarification_required", "technically_feasible",
    "documentation", "estimation", "quotation_issued", "customer_decision",
    "agreement", "awaiting_deposit", "payment_verified", "project_activated",
    "development", "testing", "delivery", "completed",
    "declined", "cancelled", "on_hold", "suspended", "terminated",
}


def _payment_payload(p: ProjectPayment) -> dict:
    return {
        "id": p.id,
        "payment_type": p.payment_type,
        "amount": float(p.amount) if p.amount is not None else None,
        "currency": p.currency,
        "status": p.status,
        "method": p.method,
        "reference": p.reference,
        "receipt_number": p.receipt_number,
        "verified_at": p.verified_at,
        "paid_at": p.paid_at,
        "created_at": p.created_at,
    }


def _request_payload(r: ProjectRequest) -> dict:
    deposit_amount = None
    if r.quotation_amount is not None:
        deposit_amount = float(r.quotation_amount) * (r.deposit_percent or 30) / 100
    return {
        "id": r.id,
        "request_number": r.request_number,
        "title": r.title,
        "description": r.description,
        "service_type": r.service_type,
        "location": r.location,
        "category": r.category,
        "status": r.status,
        "budget": float(r.budget) if r.budget is not None else None,
        "deadline": r.deadline,
        "admin_notes": r.admin_notes,
        "admin_decision": r.admin_decision,
        "quotation_amount": float(r.quotation_amount) if r.quotation_amount is not None else None,
        "quotation_currency": r.quotation_currency,
        "deposit_percent": r.deposit_percent,
        "deposit_amount": deposit_amount,
        "payment_schedule": r.payment_schedule,
        "scope_included": r.scope_included,
        "scope_excluded": r.scope_excluded,
        "quotation_version": r.quotation_version,
        "quotation_issued_at": r.quotation_issued_at,
        "quotation_accepted_at": r.quotation_accepted_at,
        "quotation_declined_at": r.quotation_declined_at,
        "agreed_amount": float(r.agreed_amount) if r.agreed_amount is not None else None,
        "paid_amount": float(r.paid_amount) if r.paid_amount is not None else 0,
        "activated_at": r.activated_at,
        "created_at": r.created_at,
        "payments": [_payment_payload(p) for p in (r.payments or [])],
    }


VALID_SERVICE_TYPES = {
    "software_development", "wifi_installation", "cctv_installation",
    "network_setup", "consultancy", "it_support", "maintenance", "other",
}


class ProjectRequestCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10, max_length=10000)
    service_type: Optional[str] = "software_development"
    location: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = None
    budget: Optional[float] = None
    deadline: Optional[date] = None


class PublicProjectRequest(BaseModel):
    """Guest project request - no account required (today.md doc 8). Can be a
    software build, a Wi-Fi/CCTV installation, consultancy, etc."""
    full_name: str = Field(min_length=3, max_length=200)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=50)
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10, max_length=10000)
    service_type: Optional[str] = "software_development"
    location: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = None
    budget: Optional[float] = None
    deadline: Optional[date] = None


class PaymentIn(BaseModel):
    payment_type: str = "deposit"
    amount: float
    method: str = "manual"
    reference: Optional[str] = None


async def _get_owned_request(db: AsyncSession, customer: Customer, request_id: str) -> ProjectRequest:
    from sqlalchemy.orm import selectinload
    r = await db.scalar(
        select(ProjectRequest)
        .options(selectinload(ProjectRequest.payments))
        .where(
            ProjectRequest.id == request_id,
            ProjectRequest.customer_id == customer.id,
        )
    )
    if not r:
        raise HTTPException(status_code=404, detail="Project request not found")
    return r


async def _next_request_number(db: AsyncSession) -> str:
    year = datetime.now().year
    count = await db.scalar(
        select(func.count()).select_from(ProjectRequest)
        .where(ProjectRequest.request_number.like(f"NOU-REQ-{year}-%"))
    ) or 0
    return f"NOU-REQ-{year}-{(count + 1):04d}"


@router.post("/projects/public-request", status_code=status.HTTP_201_CREATED)
async def public_project_request(
    body: PublicProjectRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a project request WITHOUT registering or creating an account.

    The customer record is created on the fly (the generated password is
    unusable, so this is NOT an account they can sign into until they use
    'forgot password'). N.O.U. contacts them at the email they provide.
    """
    check_rate_limit(request, "public-request:ip", max_hits=10, window_seconds=3600)
    check_rate_limit(request, f"public-request:email:{body.email}", max_hits=5, window_seconds=3600)

    parts = body.full_name.strip().split(None, 1)
    first_name = parts[0] if parts else body.email.split("@")[0]
    last_name = parts[1] if len(parts) > 1 else ""

    user = await db.scalar(select(User).where(User.email == body.email))
    if not user:
        user = User(
            email=body.email,
            password_hash=get_password_hash(uuid.uuid4().hex),
            first_name=first_name,
            last_name=last_name,
            role="customer",
            is_active=True,
            # Submitting the request constitutes agreement to the terms.
            terms_accepted_at=datetime.now(),
        )
        db.add(user)
        await db.flush()

    customer = await ensure_customer_profile(db, user)
    if body.phone and not customer.phone:
        customer.phone = body.phone

    new_project = ProjectRequest(
        customer_id=customer.id,
        title=body.title,
        description=body.description,
        service_type=body.service_type or "software_development",
        location=body.location,
        category=body.category,
        budget=body.budget,
        deadline=body.deadline,
        status="submitted",
        request_number=await _next_request_number(db),
    )
    db.add(new_project)
    # Commit before responding (read-your-writes).
    await db.commit()

    from sqlalchemy.orm import selectinload
    fresh = await db.scalar(
        select(ProjectRequest)
        .options(selectinload(ProjectRequest.payments))
        .where(ProjectRequest.id == new_project.id)
    )
    return {
        "message": (
            "Project request submitted. N.O.U. will review it and contact you "
            "at the email you provided."
        ),
        "request": _request_payload(fresh or new_project),
    }


@router.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project_request(
    body: ProjectRequestCreate,
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db)
):
    """Create a new project request with a unique request number (SUBMITTED)."""
    customer = await ensure_customer_profile(db, current_user)

    new_project = ProjectRequest(
        customer_id=customer.id,
        title=body.title,
        description=body.description,
        service_type=body.service_type or "software_development",
        location=body.location,
        category=body.category,
        budget=body.budget,
        deadline=body.deadline,
        status="submitted",
        request_number=await _next_request_number(db),
    )

    db.add(new_project)
    await db.flush()
    # Re-load with payments eager-loaded (async sessions cannot lazy-load).
    from sqlalchemy.orm import selectinload
    fresh = await db.scalar(
        select(ProjectRequest)
        .options(selectinload(ProjectRequest.payments))
        .where(ProjectRequest.id == new_project.id)
    )
    return _request_payload(fresh or new_project)


@router.get("/projects/me")
async def get_my_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db)
):
    """Current customer's project requests (with quotation + payment detail)."""
    customer = await ensure_customer_profile(db, current_user)
    from sqlalchemy.orm import selectinload

    query = (
        select(ProjectRequest)
        .options(selectinload(ProjectRequest.payments))
        .where(ProjectRequest.customer_id == customer.id)
    )
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(
        query.order_by(ProjectRequest.created_at.desc())
        .offset((page - 1) * limit).limit(limit)
    )
    projects = result.scalars().all()

    return {
        "projects": [_request_payload(p) for p in projects],
        "pagination": {
            "total": total, "page": page, "limit": limit,
            "pages": (total + limit - 1) // limit if total else 0,
        },
    }


@router.get("/projects/{project_id}")
async def get_project_request(
    project_id: str,
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db),
):
    """Single project request detail (customer)."""
    customer = await ensure_customer_profile(db, current_user)
    r = await _get_owned_request(db, customer, project_id)
    return _request_payload(r)


class QuotationDecision(BaseModel):
    pass


@router.post("/projects/{project_id}/accept-quotation")
async def accept_quotation(
    project_id: str,
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db),
):
    """Customer accepts the issued quotation -> AGREEMENT -> AWAITING DEPOSIT."""
    customer = await ensure_customer_profile(db, current_user)
    r = await _get_owned_request(db, customer, project_id)
    if r.status != "quotation_issued":
        raise HTTPException(
            status_code=400,
            detail=f"A quotation can only be accepted after it is issued (status: {r.status})",
        )
    r.status = "awaiting_deposit"
    r.quotation_accepted_at = datetime.now()
    r.agreed_amount = r.quotation_amount
    r.agreed_at = datetime.now()
    await db.commit()
    return {"message": "Quotation accepted - initial deposit now due", "request": _request_payload(r)}


@router.post("/projects/{project_id}/decline-quotation")
async def decline_quotation(
    project_id: str,
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db),
):
    """Customer declines the issued quotation."""
    customer = await ensure_customer_profile(db, current_user)
    r = await _get_owned_request(db, customer, project_id)
    if r.status != "quotation_issued":
        raise HTTPException(status_code=400, detail="No issued quotation to decline")
    r.status = "declined"
    r.quotation_declined_at = datetime.now()
    await db.commit()
    return {"message": "Quotation declined", "request": _request_payload(r)}


@router.post("/projects/{project_id}/payments", status_code=status.HTTP_201_CREATED)
async def submit_payment(
    project_id: str,
    body: PaymentIn,
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db),
):
    """Customer records a payment (e.g. the 30% initial deposit). A payment is
    only credited once an admin verifies it (today.md doc 8, sec. 20)."""
    customer = await ensure_customer_profile(db, current_user)
    r = await _get_owned_request(db, customer, project_id)
    if r.status not in ("awaiting_deposit", "payment_verified"):
        raise HTTPException(
            status_code=400,
            detail=f"Payments are only accepted after the quotation is accepted (status: {r.status})",
        )

    payment = ProjectPayment(
        project_request_id=r.id,
        payment_type=body.payment_type,
        amount=body.amount,
        currency="KSh",
        status="pending",
        method=body.method,
        reference=body.reference,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return {
        "message": "Payment submitted for verification",
        "payment": _payment_payload(payment),
    }
