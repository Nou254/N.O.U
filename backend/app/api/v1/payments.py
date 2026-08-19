"""
Payments API - M-Pesa Daraja C2B (STK push) and Flutterwave (cards).

- ``POST /payments/initiate`` (customer): creates a ProjectPayment and starts
  the chosen provider flow (M-Pesa STK push to the phone / Flutterwave
  checkout link). While provider keys are unset the providers run in
  simulation mode (payment recorded as processing, no real charge).
- ``POST /payments/support`` (public): lets anyone contribute/support the
  company through the same M-Pesa / Flutterwave gateways. Used from the
  footer Support section.
- ``POST /payments/mpesa/callback`` + ``/payments/mpesa/validation``: Daraja
  C2B endpoints (public, signature/result-code guarded).
- ``POST /payments/flutterwave/webhook``: Flutterwave webhook
  (verif-hash guarded).
- ``GET /payments/status``: provider configuration status (admin).

A successful provider confirmation finalizes the payment: official NOU-RCP
receipt, project credited and activated (see services/payments.py).
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.core.config import settings
from app.core.security import require_customer, require_admin
from app.core.rate_limit import check_rate_limit
from app.models.user import User
from app.models.project_request import ProjectRequest, ProjectPayment
from app.models.customer import Customer
from app.services.payments import (
    initiate_mpesa_stk_push, initiate_flutterwave_payment,
    handle_mpesa_callback, handle_flutterwave_webhook, payments_status,
)

router = APIRouter()


class PaymentInitiate(BaseModel):
    project_request_id: str
    payment_type: str = "deposit"
    amount: float = Field(..., gt=0)
    method: str = Field(..., pattern="^(mpesa|card)$")
    currency: str = "KSh"
    # M-Pesa only
    phone: Optional[str] = Field(None, max_length=20)
    # Flutterwave only (falls back to the customer's account email)
    email: Optional[EmailStr] = None


async def _owned_request(
    db: AsyncSession, customer: Customer, request_id: str
) -> ProjectRequest:
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


def _payment_payload(p: ProjectPayment) -> dict:
    return {
        "id": p.id,
        "payment_type": p.payment_type,
        "amount": float(p.amount) if p.amount is not None else None,
        "currency": p.currency,
        "status": p.status,
        "method": p.method,
        "reference": p.reference,
        "provider_reference": p.provider_reference,
        "receipt_number": p.receipt_number,
        "verified_at": p.verified_at,
        "paid_at": p.paid_at,
        "created_at": p.created_at,
    }


@router.post("/payments/initiate", status_code=201)
async def initiate_payment(
    body: PaymentInitiate,
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db),
):
    """Start a provider payment (M-Pesa STK push or Flutterwave card)."""
    from sqlalchemy.orm import selectinload
    from app.api.v1.auth import _safe_user

    customer = await db.scalar(
        select(Customer).where(Customer.user_id == current_user.id)
    )
    if not customer:
        raise HTTPException(status_code=400, detail="Customer profile not found")

    r = await _owned_request(db, customer, body.project_request_id)
    if r.status not in ("awaiting_deposit", "payment_verified"):
        raise HTTPException(
            status_code=400,
            detail=f"Payments are only accepted after the quotation is accepted (status: {r.status})",
        )

    payment = ProjectPayment(
        project_request_id=r.id,
        payment_type=body.payment_type,
        amount=body.amount,
        currency=body.currency or "KSh",
        status="processing",
        method=body.method,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    safe = _safe_user(current_user)
    customer_name = f"{safe.get('first_name', '')} {safe.get('last_name', '')}".strip()
    description = f"N.O.U {r.request_number} {body.payment_type}"

    try:
        if body.method == "mpesa":
            if not body.phone:
                raise HTTPException(
                    status_code=422,
                    detail="Phone number is required for M-Pesa (STK push)",
                )
            result = await initiate_mpesa_stk_push(
                db, payment.id, body.amount, body.phone, description
            )
        else:
            email = body.email or safe.get("email")
            result = await initiate_flutterwave_payment(
                db, payment.id, body.amount, body.currency or "KES",
                email or "", customer_name or email or "customer",
                description,
            )
    except HTTPException:
        # Leave the payment row for an admin to see, but re-raise the error.
        payment.status = "failed"
        await db.commit()
        raise
    except Exception as exc:  # noqa: BLE001 - provider/network failure
        payment.status = "failed"
        await db.commit()
        raise HTTPException(
            status_code=502,
            detail=f"Payment provider error: {str(exc)[:200]}",
        )

    payment.provider_reference = result.get("provider_reference")
    await db.commit()

    return {
        "message": result.get("message", "Payment initiated"),
        "simulated": result.get("simulated", False),
        "checkout_url": result.get("checkout_url"),
        "payment": _payment_payload(payment),
    }


class SupportContribution(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    amount: float = Field(..., gt=0)
    method: str = Field(..., pattern="^(mpesa|card)$")
    currency: str = "KSh"
    message: Optional[str] = Field(None, max_length=1000)


@router.post("/payments/support", status_code=201)
async def support_contribution(
    body: SupportContribution,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Public support/contribution payment from the footer Support section. No
    account or project is required - the same M-Pesa / Flutterwave gateways
    are used and the contribution is recorded for the admin dashboard.
    """
    check_rate_limit(request, "support:ip", max_hits=5, window_seconds=3600)

    payment = ProjectPayment(
        project_request_id=None,
        payment_type="support",
        amount=body.amount,
        currency=body.currency or "KSh",
        status="processing",
        method=body.method,
        notes=(
            f"Support contribution from {body.full_name} ({body.email})"
            + (f" - {body.message[:200]}" if body.message else "")
        ),
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    # Flutterwave requires ISO 4217 currency codes (KES), not the KSh symbol.
    flutterwave_currency = "KES" if (body.currency or "KSh") == "KSh" else (body.currency or "KES")
    description = "N.O.U support contribution"
    try:
        if body.method == "mpesa":
            if not body.phone:
                raise HTTPException(
                    status_code=422,
                    detail="Phone number is required for M-Pesa (STK push)",
                )
            result = await initiate_mpesa_stk_push(
                db, payment.id, body.amount, body.phone, description
            )
        else:
            result = await initiate_flutterwave_payment(
                db, payment.id, body.amount, flutterwave_currency,
                body.email, body.full_name, description,
                redirect_url=f"{settings.FRONTEND_BASE_URL}/support?paid={payment.id}",
            )
    except HTTPException:
        payment.status = "failed"
        await db.commit()
        raise
    except Exception as exc:  # noqa: BLE001 - provider/network failure
        payment.status = "failed"
        await db.commit()
        raise HTTPException(
            status_code=502,
            detail=f"Payment provider error: {str(exc)[:200]}",
        )

    payment.provider_reference = result.get("provider_reference")
    await db.commit()

    return {
        "message": result.get("message", "Payment initiated"),
        "simulated": result.get("simulated", False),
        "checkout_url": result.get("checkout_url"),
        "payment": _payment_payload(payment),
    }


class SupportPledge(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    amount: Optional[float] = Field(None, gt=0)
    reference: Optional[str] = Field(None, max_length=120)
    message: Optional[str] = Field(None, max_length=1000)


@router.post("/payments/support/pledge", status_code=201)
async def support_pledge(
    body: SupportPledge,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Public support pledge. Online payment is not processed on the site yet, so
    supporters are asked to forward their contribution via M-Pesa to the
    company number and notify us here - the pledge is recorded for the admin
    to confirm receipt (no STK push, no card charge).
    """
    check_rate_limit(request, "support:ip", max_hits=5, window_seconds=3600)

    payment = ProjectPayment(
        project_request_id=None,
        payment_type="support",
        amount=body.amount or 0,
        currency="KSh",
        status="pending",
        method="mpesa_manual",
        reference=body.reference,
        notes=(
            f"Support pledge from {body.full_name}"
            + (f" ({body.phone})" if body.phone else "")
            + (f" - {body.message[:200]}" if body.message else "")
        ),
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return {
        "message": (
            "Thank you! Forward your contribution via M-Pesa to 0796298662 "
            "and our team will confirm receipt."
        ),
        "payment": {
            "id": payment.id,
            "amount": float(payment.amount),
            "currency": payment.currency,
            "status": payment.status,
            "method": payment.method,
        },
    }


@router.post("/payments/mpesa/validation")
async def mpesa_validation(payload: dict):
    """Daraja C2B validation endpoint - accept the transaction."""
    return {"ResultCode": 0, "ResultDesc": "Success"}


@router.post("/payments/mpesa/callback")
async def mpesa_callback(payload: dict, db: AsyncSession = Depends(get_db)):
    """Daraja C2B / STK callback - confirms the payment and activates it."""
    result = await handle_mpesa_callback(db, payload)
    if not result.get("success"):
        return {"ResultCode": 1, "ResultDesc": result.get("message", "Failed")}
    return {"ResultCode": 0, "ResultDesc": "Success", **result}


@router.post("/payments/flutterwave/webhook")
async def flutterwave_webhook(
    payload: dict,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Flutterwave webhook - verifies the hash and finalizes completed charges."""
    signature = request.headers.get("verif-hash")
    return await handle_flutterwave_webhook(db, payload, signature)


@router.get("/payments/status")
async def payment_provider_status(
    current_user: User = Depends(require_admin),
):
    """Provider configuration status (admin debug)."""
    return payments_status()
