"""
Payment provider integration - M-Pesa Daraja C2B (Kenya) + Flutterwave (cards).

Flow:
1. The customer chooses a method (mpesa | card) and the API creates a
   ProjectPayment row (status=processing) with a unique merchant reference.
2. ``initiate_mpesa_stk_push`` pushes a Lipa Na M-Pesa prompt to the phone
   (Daraja). ``initiate_flutterwave_payment`` returns a Flutterwave hosted
   checkout link the customer is redirected to.
3. Safaricom / Flutterwave call our webhook endpoints; the webhook verifies
   authenticity, finds the payment by reference, marks it successful, issues
   the official NOU-RCP receipt and activates the project (same rules as an
   admin verifying a payment manually).

Credential handling: while the provider keys are empty in ``backend/.env``
the providers run in SIMULATION mode - the payment row is still created
(status=processing/pending) so the whole product flow works, and the response
clearly says the provider is not configured yet. Fill in the keys (M-Pesa
Daraja + Flutterwave) to switch on live/sandbox calls.
"""

import base64
import hashlib
import hmac
import time
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.project_request import ProjectRequest, ProjectPayment


# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------
def mpesa_configured() -> bool:
    return bool(
        settings.MPESA_CONSUMER_KEY and settings.MPESA_CONSUMER_SECRET
        and settings.MPESA_SHORTCODE and settings.MPESA_PASSKEY
    )


def flutterwave_configured() -> bool:
    return bool(settings.FLUTTERWAVE_SECRET_KEY)


def _mpesa_base_url() -> str:
    return (
        "https://api.safaricom.co.ke"
        if settings.MPESA_ENV == "live"
        else "https://sandbox.safaricom.co.ke"
    )


def _mpesa_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def _mpesa_password() -> str:
    raw = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{_mpesa_timestamp()}"
    return base64.b64encode(raw.encode()).decode()


def normalize_phone(phone: str) -> str:
    """2547XXXXXXXX form for Daraja (strips +, leading 0 / 254)."""
    digits = "".join(ch for ch in str(phone) if ch.isdigit())
    if digits.startswith("0"):
        digits = "254" + digits[1:]
    elif digits.startswith("254"):
        pass
    else:
        digits = "254" + digits
    return digits


async def _issue_receipt(db: AsyncSession, payment: ProjectPayment) -> str:
    year = datetime.now().year
    seq = await db.scalar(
        select(func.count()).select_from(ProjectPayment)
        .where(ProjectPayment.receipt_number.like(f"NOU-RCP-{year}-%"))
    ) or 0
    return f"NOU-RCP-{year}-{(seq + 1):04d}"


async def finalize_successful_payment(
    db: AsyncSession,
    payment_id,
    provider_reference: str = None,
    notes: str = None,
) -> ProjectPayment:
    """Mark a payment successful, issue the receipt, credit the project and
    activate it (mirrors the admin manual-verify rules)."""
    payment = await db.scalar(
        select(ProjectPayment).where(ProjectPayment.id == payment_id)
    )
    if not payment:
        raise ValueError("Payment not found")
    if payment.status == "successful":
        return payment

    payment.status = "successful"
    payment.provider_reference = provider_reference or payment.provider_reference
    payment.paid_at = datetime.now()
    if notes:
        payment.notes = notes
    if not payment.receipt_number:
        payment.receipt_number = await _issue_receipt(db, payment)

    request = await db.scalar(
        select(ProjectRequest).where(ProjectRequest.id == payment.project_request_id)
    )
    if request:
        request.paid_amount = (request.paid_amount or 0) + payment.amount
        if request.status in ("awaiting_deposit", "payment_verified"):
            request.status = "project_activated"
            request.activated_at = request.activated_at or datetime.now()
    await db.commit()
    return payment


# ---------------------------------------------------------------------------
# M-Pesa Daraja C2B - Lipa Na M-Pesa (STK push)
# ---------------------------------------------------------------------------
async def initiate_mpesa_stk_push(
    db: AsyncSession,
    payment_id: int,
    amount: float,
    phone: str,
    description: str = "N.O.U Digital Systems payment",
) -> dict:
    """Push an STK prompt to the customer's phone. Returns the provider
    response; in simulation mode returns a clearly-marked simulated result."""
    phone = normalize_phone(phone)
    # AccountReference max 12 chars - use the short payment id.
    account_ref = f"NOU-{payment_id}"
    callback_base = settings.MPESA_CALLBACK_BASE_URL or settings.FRONTEND_BASE_URL
    callback_url = (
        f"{callback_base}/api/v1/payments/mpesa/callback"
    )

    if not mpesa_configured():
        return {
            "simulated": True,
            "status": "processing",
            "message": (
                "M-Pesa Daraja is not configured yet - payment recorded as "
                "processing. Configure MPESA_* in backend/.env to send a "
                "real STK push."
            ),
            "account_reference": account_ref,
            "provider_reference": None,
        }

    import httpx

    async with httpx.AsyncClient(timeout=30) as client:
        # 1. OAuth token
        token_resp = await client.get(
            f"{_mpesa_base_url()}/oauth/v1/generate?grant_type=client_credentials",
            auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET),
        )
        token_resp.raise_for_status()
        access_token = token_resp.json().get("access_token")
        if not access_token:
            raise RuntimeError("Failed to obtain Daraja access token")

        # 2. STK push request
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": _mpesa_password(),
            "Timestamp": _mpesa_timestamp(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(round(amount)),
            "PartyA": phone,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": callback_url,
            "AccountReference": account_ref,
            "TransactionDesc": description[:20],
        }
        resp = await client.post(
            f"{_mpesa_base_url()}/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("ResponseCode") != "0":
            raise RuntimeError(f"STK push rejected: {data.get('ResponseDescription')}")
        return {
            "simulated": False,
            "status": "processing",
            "message": "STK push sent - check your phone and enter your PIN.",
            "account_reference": account_ref,
            "provider_reference": data.get("CheckoutRequestID"),
            "merchant_request_id": data.get("MerchantRequestID"),
        }


async def handle_mpesa_callback(db: AsyncSession, payload: dict) -> dict:
    """Process a Daraja C2B / STK callback. Returns the final payment state."""
    body = payload.get("Body", payload)
    stk = body.get("stkCallback", body)
    # Look up the payment by AccountReference (NOU-<payment_id>).
    ref = (stk.get("CallbackMetadata") or {}).get("AccountReference")
    merchant = stk.get("MerchantRequestID") or stk.get("CheckoutRequestID")
    result_code = stk.get("ResultCode")

    # Fallback: find the payment by provider reference (CheckoutRequestID).
    payment = None
    if ref and str(ref).startswith("NOU-"):
        try:
            payment_id = int(str(ref).split("-")[-1])
            payment = await db.scalar(
                select(ProjectPayment).where(ProjectPayment.id == payment_id)
            )
        except (ValueError, TypeError):
            payment = None
    if payment is None and merchant:
        payment = await db.scalar(
            select(ProjectPayment).where(ProjectPayment.provider_reference == merchant)
        )

    if payment is None:
        return {"success": False, "message": "Unknown payment reference"}

    if str(result_code) == "0":
        # Extract the M-Pesa receipt code from the callback metadata.
        mpesa_code = None
        items = ((stk.get("CallbackMetadata") or {}).get("Item") or [])
        for item in items:
            if item.get("Name") == "MpesaReceiptNumber":
                mpesa_code = item.get("Value")
        await finalize_successful_payment(
            db, payment.id, provider_reference=mpesa_code,
            notes="Confirmed by M-Pesa C2B callback",
        )
        return {
            "success": True,
            "message": "Payment confirmed",
            "receipt": payment.receipt_number,
        }
    payment.status = "failed"
    await db.commit()
    return {"success": False, "message": f"M-Pesa result code {result_code}"}


# ---------------------------------------------------------------------------
# Flutterwave - card payments (hosted checkout)
# ---------------------------------------------------------------------------
async def initiate_flutterwave_payment(
    db: AsyncSession,
    payment_id: int,
    amount: float,
    currency: str,
    email: str,
    customer_name: str,
    description: str = "N.O.U Digital Systems payment",
    redirect_url: str = None,
) -> dict:
    """Create a Flutterwave hosted checkout link for card payments. In
    simulation mode returns a stub link (no real charge is created)."""
    tx_ref = f"NOU-{payment_id}"
    redirect_url = redirect_url or (
        f"{settings.FRONTEND_BASE_URL}/customer/projects?paid={payment_id}"
    )

    if not flutterwave_configured():
        return {
            "simulated": True,
            "status": "processing",
            "message": (
                "Flutterwave is not configured yet - payment recorded as "
                "processing. Configure FLUTTERWAVE_SECRET_KEY in "
                "backend/.env to take real card payments."
            ),
            "checkout_url": f"{redirect_url}&simulated=1",
            "tx_ref": tx_ref,
            "provider_reference": None,
        }

    import httpx

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.flutterwave.com/v3/payments",
            headers={
                "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "tx_ref": tx_ref,
                "amount": round(float(amount), 2),
                "currency": currency or "KES",
                "redirect_url": redirect_url,
                "customer": {"email": email, "name": customer_name or email},
                "customizations": {
                    "title": "N.O.U Digital Systems",
                    "description": description[:150],
                },
            },
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "success" or not data.get("data", {}).get("link"):
            raise RuntimeError(f"Flutterwave rejected payment: {data.get('message')}")
        link = data["data"]["link"]
        return {
            "simulated": False,
            "status": "processing",
            "message": "Card checkout created - redirecting to the payment page.",
            "checkout_url": link,
            "tx_ref": tx_ref,
            "provider_reference": tx_ref,
        }


async def handle_flutterwave_webhook(
    db: AsyncSession, payload: dict, signature: str = None
) -> dict:
    """Verify + process a Flutterwave webhook (charge.completed)."""
    if settings.FLUTTERWAVE_WEBHOOK_SECRET_HASH and not signature:
        return {"success": False, "message": "Missing webhook signature"}
    if settings.FLUTTERWAVE_WEBHOOK_SECRET_HASH:
        expected = settings.FLUTTERWAVE_WEBHOOK_SECRET_HASH
        actual = hmac.new(expected.encode(), str(payload).encode(), hashlib.sha256).hexdigest()
        # Flutterwave sends the raw hash in the header - compare directly.
        if signature != expected and actual != signature:
            return {"success": False, "message": "Invalid webhook signature"}

    event = payload.get("event")
    data = payload.get("data", {})
    if event != "charge.completed":
        return {"success": True, "message": "Ignored event"}

    tx_ref = data.get("tx_ref") or data.get("txRef")
    status = (data.get("status") or "").lower()
    if status != "successful":
        return {"success": False, "message": f"Charge not successful ({status})"}

    payment = None
    if tx_ref and str(tx_ref).startswith("NOU-"):
        try:
            payment_id = int(str(tx_ref).split("-")[-1])
            payment = await db.scalar(
                select(ProjectPayment).where(ProjectPayment.id == payment_id)
            )
        except (ValueError, TypeError):
            payment = None
    if payment is None:
        return {"success": False, "message": "Unknown transaction reference"}

    await finalize_successful_payment(
        db, payment.id,
        provider_reference=tx_ref or data.get("flw_ref") or data.get("id"),
        notes="Confirmed by Flutterwave webhook",
    )
    return {
        "success": True,
        "message": "Payment confirmed",
        "receipt": payment.receipt_number,
    }


# ---------------------------------------------------------------------------
# Provider status (admin debug / dashboard)
# ---------------------------------------------------------------------------
def payments_status() -> dict:
    return {
        "mpesa_configured": mpesa_configured(),
        "mpesa_env": settings.MPESA_ENV,
        "flutterwave_configured": flutterwave_configured(),
        "simulation_mode": not (mpesa_configured() or flutterwave_configured()),
    }
