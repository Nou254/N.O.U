"""
N.O.U Lite - the website's AI customer assistant.

Inspired by the WhatsApp chatbot (My_Whatsapp_Chatbot/index.js): customers
chat with the assistant, which takes their orders (products, projects,
support). Each conversation that results in an order is persisted for admin
review via /api/v1/admin/nou-lite/orders.

The assistant uses Groq through the shared key pool (nou_lite section,
10 keys/day + 2 top-up) and keeps a short per-customer conversation history
in memory.
"""

import json
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import check_rate_limit
from app.core.security import get_current_user, get_optional_user
from app.models.user import User
from app.models.nou_lite_order import NouliteOrder

logger = logging.getLogger("nou_lite")

router = APIRouter()

SYSTEM_PROMPT = (
    "You are N.O.U Lite, the friendly AI assistant for N.O.U Digital Systems. "
    "N.O.U Digital Systems operates digitally and handles all inquiries "
    "remotely via Phone/WhatsApp (0796 298 662) and Email "
    "(noudigitalsystem@gmail.com). Never mention a physical office address. "
    "You help customers with: (1) software products and downloads, "
    "(2) requesting software projects, (3) support and bug reports, "
    "(4) general company information. When a customer wants to place an "
    "order or request (a product purchase, a project build, or a support "
    "issue), gather the essential details by asking 1-2 clarifying questions "
    "if needed, then reply with ONLY a JSON object in exactly this shape "
    "wrapped in <ORDER>...</ORDER> tags:\n"
    '<ORDER>{"order_type": "product|project|support|inquiry", '
    '"summary": "one line order summary", '
    '"details": {"product": "name", "requirements": "...", "notes": "..."}}</ORDER>\n'
    "along with a short friendly confirmation message before the tags. "
    "If the request is just a question, answer helpfully without ORDER tags."
)

# Per-customer short conversation memory: email -> list of {role, content}
_history: dict = {}
MAX_HISTORY = 8


class ChatIn(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    # Optional for guests (no account). Logged-in customers are identified by
    # their token; guests must supply an email so their order can be followed
    # up by the admin.
    email: Optional[str] = Field(None, max_length=255)


async def _call_groq(messages: list) -> str:
    from app.services.groq_pool import get_client, mark_failed
    from groq import AuthenticationError
    from app.core.config import settings

    client, key_index = await get_client("nou_lite")
    try:
        resp = await client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=messages,
            temperature=0.5,
            max_tokens=700,
        )
        return (resp.choices[0].message.content or "").strip()
    except AuthenticationError:
        mark_failed("nou_lite", key_index)
        raise
    except Exception as exc:  # noqa: BLE001
        logger.warning("nou_lite groq error: %s", exc)
        raise


def _parse_order(content: str) -> Optional[dict]:
    """Extract the <ORDER>...</ORDER> JSON payload if present."""
    start = content.find("<ORDER>")
    end = content.rfind("</ORDER>")
    if start == -1 or end == -1:
        return None
    raw = content[start + len("<ORDER>"):end].strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


@router.post("/chat")
async def chat(
    body: ChatIn,
    request: Request,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Send a message to N.O.U Lite (guests welcome - no login required).

    If the conversation results in an order it is saved for admin review.
    Guests are identified by the email they provide; logged-in customers are
    identified by their token.
    """
    check_rate_limit(request, "nou_lite:user", max_hits=60, window_seconds=3600)

    # N.O.U Lite is open to everyone - no login/account required. Guests may
    # optionally provide an email so their order can be followed up; without
    # one we fall back to a session identifier so orders are still recorded
    # for admin review.
    guest = current_user is None
    email = body.email or (current_user.email if current_user else None) \
        or f"guest:{request.client.host}"

    history = _history.setdefault(email, [])
    history.append({"role": "user", "content": body.message})
    history = history[-MAX_HISTORY:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        reply = await _call_groq(messages)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=502, detail="N.O.U Lite is temporarily unavailable. Please try again.")

    history.append({"role": "assistant", "content": reply})
    _history[email] = history[-MAX_HISTORY:]

    order = _parse_order(reply)
    created_order = None
    if order:
        order_type = str(order.get("order_type", "inquiry"))
        if order_type not in ("product", "project", "support", "inquiry"):
            order_type = "inquiry"
        details = order.get("details") or {}
        created_order = NouliteOrder(
            customer_id=current_user.id if current_user else None,
            guest_email=email if guest else None,
            order_type=order_type,
            summary=str(order.get("summary", ""))[:1000] or "N.O.U Lite order",
            details=json.dumps(details)[:4000],
            status="new",
            ai_transcript=json.dumps(history[-MAX_HISTORY:], ensure_ascii=False)[:10000],
        )
        db.add(created_order)
        await db.commit()
        await db.refresh(created_order)
        # Keep the friendly reply text (strip the ORDER block).
        reply = reply[:start] if (start := reply.find("<ORDER>")) != -1 else reply

    return {
        "reply": reply.strip(),
        "order_created": created_order is not None,
        "order": ({
            "id": created_order.id,
            "order_type": created_order.order_type,
            "summary": created_order.summary,
        } if created_order else None),
    }


@router.get("/orders")
async def my_orders(
    current_user: Optional[User] = Depends(get_optional_user),
    email: Optional[str] = Query(None, max_length=255),
    db: AsyncSession = Depends(get_db),
):
    """A customer's N.O.U Lite orders.

    Logged-in customers are identified by their token. Guests (no account
    needed) pass the email they supplied when chatting so they can track
    their orders.
    """
    stmt = select(NouliteOrder)
    if current_user:
        stmt = stmt.where(NouliteOrder.customer_id == current_user.id)
    elif email and email.strip():
        stmt = stmt.where(NouliteOrder.guest_email == email.strip())
    else:
        return {"orders": []}
    result = await db.execute(stmt.order_by(NouliteOrder.created_at.desc()))
    orders = result.scalars().all()
    return {"orders": [{
        "id": o.id,
        "order_type": o.order_type,
        "summary": o.summary,
        "details": o.details,
        "status": o.status,
        "created_at": o.created_at,
    } for o in orders]}
