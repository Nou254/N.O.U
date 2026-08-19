"""
Customers API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user, require_customer, ensure_customer_profile
from app.models.user import User
from app.models.customer import Customer

router = APIRouter()


@router.get("/me")
async def get_customer_profile(
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current customer profile.
    """
    # Get (or lazily create) the customer profile
    customer = await ensure_customer_profile(db, current_user)
    
    return customer


@router.put("/me")
async def update_customer_profile(
    company_name: Optional[str] = None,
    phone: Optional[str] = None,
    address: Optional[str] = None,
    city: Optional[str] = None,
    country: Optional[str] = None,
    current_user: User = Depends(require_customer),
    db: AsyncSession = Depends(get_db)
):
    """
    Update customer profile.
    """
    # Get (or lazily create) the customer profile
    customer = await ensure_customer_profile(db, current_user)
    
    # Update fields
    if company_name is not None:
        customer.company_name = company_name
    if phone is not None:
        customer.phone = phone
    if address is not None:
        customer.address = address
    if city is not None:
        customer.city = city
    if country is not None:
        customer.country = country
    
    await db.flush()
    await db.refresh(customer)
    
    return customer