"""
Support API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user, require_customer, require_admin, ensure_customer_profile
from app.models.user import User
from app.models.support import SupportTicket

router = APIRouter()


class TicketCreate(BaseModel):
    subject: str
    description: str
    category: Optional[str] = "general"
    priority: Optional[str] = "medium"


@router.post("/tickets", status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket: TicketCreate,
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a support ticket.
    """
    # Get (or lazily create) the customer profile
    customer = await ensure_customer_profile(db, current_user)
    
    # Create ticket
    new_ticket = SupportTicket(
        customer_id=customer.id,
        subject=ticket.subject,
        description=ticket.description,
        category=ticket.category,
        priority=ticket.priority
    )
    
    db.add(new_ticket)
    await db.flush()
    await db.refresh(new_ticket)
    
    return new_ticket


@router.get("/tickets/me")
async def get_my_tickets(
    status_filter: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's support tickets.
    """
    # Get (or lazily create) the customer profile
    customer = await ensure_customer_profile(db, current_user)
    
    query = select(SupportTicket).where(SupportTicket.customer_id == customer.id)
    
    if status_filter:
        query = query.where(SupportTicket.status == status_filter)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    # Apply pagination and ordering
    query = query.order_by(SupportTicket.created_at.desc())
    query = query.offset((page - 1) * limit).limit(limit)
    
    result = await db.execute(query)
    tickets = result.scalars().all()
    
    return {
        "tickets": tickets,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    }


@router.get("/tickets/{ticket_id}")
async def get_ticket(
    ticket_id: str,
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db)
):
    """
    Get support ticket details.
    """
    # Get (or lazily create) the customer profile
    customer = await ensure_customer_profile(db, current_user)
    
    result = await db.execute(
        select(SupportTicket).where(
            SupportTicket.id == ticket_id,
            SupportTicket.customer_id == customer.id
        )
    )
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support ticket not found"
        )
    
    return ticket


@router.post("/tickets/{ticket_id}/reply")
async def reply_to_ticket(
    ticket_id: str,
    content: str,
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db)
):
    """
    Reply to a support ticket.
    """
    # Get (or lazily create) the customer profile
    customer = await ensure_customer_profile(db, current_user)
    
    # Get ticket
    result = await db.execute(
        select(SupportTicket).where(
            SupportTicket.id == ticket_id,
            SupportTicket.customer_id == customer.id
        )
    )
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support ticket not found"
        )
    
    # Update ticket status
    ticket.status = "waiting_customer"
    ticket.updated_at = datetime.utcnow()
    
    await db.flush()
    
    return {"message": "Reply sent successfully"}