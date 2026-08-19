"""
Investor funding-interest model.

Captures expressions of interest from investors who want to fund the company.
Submissions come from the public /investors page and are reviewed by admins
from the admin dashboard.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, Boolean
from sqlalchemy.sql import func

from app.core.database import Base


class InvestorInterest(Base):
    __tablename__ = "investor_interests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    country = Column(String(100), nullable=False)
    organization = Column(String(255))
    investment_amount = Column(Numeric(14, 2))
    investment_range = Column(String(100))
    # Additional investor questions
    monthly_investment = Column(Numeric(14, 2))      # how much they can invest per month
    expectations = Column(Text)                      # expectations while joining the company
    risk_knowledge = Column(String(50))              # e.g. beginner / moderate / experienced
    # KSh 500 joining fee for the first month
    joining_fee_paid = Column(Boolean, default=False)
    joining_fee_paid_at = Column(DateTime)
    joining_fee_amount = Column(Numeric(10, 2), default=500)
    message = Column(Text)
    status = Column(String(20), default="new")
    admin_notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<InvestorInterest {self.full_name} ({self.country})>"
