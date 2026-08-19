"""
Investor funding-interest API endpoints.

The public /investors page lets investors submit their details if they are
interested in funding the company. Submissions land in the admin dashboard
(see /api/v1/admin/investors) for review.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import check_rate_limit
from app.models.investor import InvestorInterest

router = APIRouter()


class InvestorInterestCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=50)
    country: str = Field(..., min_length=2, max_length=100)
    organization: Optional[str] = Field(None, max_length=255)
    investment_amount: Optional[float] = Field(None, gt=0, le=1_000_000_000)
    investment_range: Optional[str] = Field(None, max_length=100)
    monthly_investment: Optional[float] = Field(None, gt=0, le=1_000_000_000)
    expectations: Optional[str] = Field(None, max_length=5000)
    risk_knowledge: Optional[str] = Field(None, max_length=50)
    message: Optional[str] = Field(None, max_length=5000)

    @field_validator("full_name")
    @classmethod
    def name_not_blank(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Name must be at least 2 characters")
        return value

    @field_validator("country")
    @classmethod
    def country_not_blank(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Country must be at least 2 characters")
        return value


@router.post("/interest", status_code=status.HTTP_201_CREATED)
async def create_investor_interest(
    body: InvestorInterestCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Record an investor's funding interest. Public (no account required);
    rate-limited per IP to prevent spam.
    """
    check_rate_limit(request, "investor:ip", max_hits=10, window_seconds=3600)

    new_interest = InvestorInterest(
        full_name=body.full_name.strip(),
        email=body.email,
        phone=body.phone,
        country=body.country.strip(),
        organization=body.organization,
        investment_amount=body.investment_amount,
        investment_range=body.investment_range,
        monthly_investment=body.monthly_investment,
        expectations=body.expectations,
        risk_knowledge=body.risk_knowledge,
        message=body.message,
        status="new",
    )
    db.add(new_interest)
    await db.flush()
    await db.refresh(new_interest)

    # Commit before responding (get_db()'s post-yield commit runs after the
    # response is sent - an explicit commit keeps the row visible to the
    # admin dashboard immediately).
    await db.commit()

    return {
        "id": new_interest.id,
        "message": "Thank you! Your investment interest has been recorded. "
                   "Our team will reach out to you soon.",
    }
