"""
Project request model (customer custom-development requests) with the full
N.O.U. quotation / payment lifecycle (today.md docs 8 + 9):

SUBMITTED -> UNDER REVIEW -> CLARIFICATION REQUIRED -> TECHNICALLY FEASIBLE
-> DOCUMENTATION -> ESTIMATION -> QUOTATION ISSUED -> CUSTOMER DECISION
-> AGREEMENT -> AWAITING DEPOSIT -> PAYMENT VERIFIED -> PROJECT ACTIVATED
-> DEVELOPMENT -> TESTING -> DELIVERY -> COMPLETED

Terminal / paused: DECLINED, CANCELLED, ON HOLD, SUSPENDED, TERMINATED.

A project enters development only after review, documentation, quotation,
customer acceptance, agreement and the verified initial deposit (30% default).
"""

from sqlalchemy import Column, String, Text, DateTime, Date, Numeric, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProjectRequest(Base):
    __tablename__ = "project_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    # The service the customer is requesting: software_development (default),
    # wifi_installation, cctv_installation, consultancy, network_setup,
    # it_support, maintenance, other.
    service_type = Column(String(50), default="software_development", index=True)
    # Physical site for installation/consultancy services (e.g. Wi-Fi/CCTV).
    location = Column(String(255))
    category = Column(String(50))
    status = Column(String(40), default="submitted", index=True)
    # Unique request number, e.g. NOU-REQ-2026-0048.
    request_number = Column(String(30), index=True)
    budget = Column(Numeric(12, 2))
    deadline = Column(Date)
    requirements_file = Column(String(500))
    admin_notes = Column(Text)

    # ---- Quotation fields (today.md) ----
    quotation_amount = Column(Numeric(14, 2))
    quotation_currency = Column(String(10), default="KSh")
    deposit_percent = Column(Integer, default=30)
    payment_schedule = Column(Text)      # human-readable payment schedule
    scope_included = Column(Text)        # what N.O.U. will deliver
    scope_excluded = Column(Text)        # what is not included
    quotation_version = Column(Integer, default=1)
    quotation_issued_at = Column(DateTime)
    quotation_accepted_at = Column(DateTime)
    quotation_declined_at = Column(DateTime)
    # Admin decisions recorded through the workflow.
    admin_decision = Column(Text)
    decision_at = Column(DateTime)

    # ---- Financials ----
    agreed_amount = Column(Numeric(14, 2))
    agreed_at = Column(DateTime)
    paid_amount = Column(Numeric(14, 2), default=0)
    activated_at = Column(DateTime)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="project_requests")
    payments = relationship(
        "ProjectPayment", back_populates="project_request",
        cascade="all, delete-orphan", order_by="ProjectPayment.created_at",
    )

    def __repr__(self):
        return f"<ProjectRequest {self.request_number or self.title}>"


class ProjectPayment(Base):
    """A payment against a customer project (deposit / milestone / final) or
    a support contribution (project_request_id is NULL for support)."""
    __tablename__ = "project_payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_request_id = Column(
        Integer, ForeignKey("project_requests.id", ondelete="CASCADE"),
        nullable=True, index=True,
    )
    payment_type = Column(String(20), default="deposit")  # deposit / milestone / final
    amount = Column(Numeric(14, 2), nullable=False)
    currency = Column(String(10), default="KSh")
    # pending / processing / successful / failed / cancelled / refunded / overdue
    status = Column(String(20), default="pending", index=True)
    method = Column(String(20))            # mpesa / bank / card / manual
    reference = Column(String(120))        # customer-provided transaction reference
    provider_reference = Column(String(120))
    receipt_number = Column(String(30), index=True)  # NOU-RCP-2026-0048
    verified_by = Column(Integer)
    verified_at = Column(DateTime)
    paid_at = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    project_request = relationship("ProjectRequest", back_populates="payments")

    def __repr__(self):
        return f"<ProjectPayment {self.receipt_number or self.reference} {self.amount}>"
