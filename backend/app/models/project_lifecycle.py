"""
Project staffing and change-request models (today.md - PROJECT STAFFING AND
TEAM FORMATION POLICY + CHANGE REQUEST PORTAL).

- StaffingPlanItem: one required position on a project (position, count,
  skills, experience level, availability, duration). The approved staffing
  plan determines who is eligible to see the project opportunity.
- ExpressionOfInterest: a qualified personnel member signals interest in a
  project opportunity. Expression of interest is NOT assignment - final
  selection remains an authorized management decision.
- ProjectChangeRequest: a controlled change to an approved project (scope
  creep protection). Customer/team requests -> impact analysis -> technical
  review -> cost/time impact -> approval -> documentation update.
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Numeric, ForeignKey, Boolean,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class StaffingPlanItem(Base):
    __tablename__ = "staffing_plan_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(
        Integer, ForeignKey("company_projects.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    position = Column(String(120), nullable=False)          # e.g. Backend Developer
    count_required = Column(Integer, nullable=False, default=1)
    skills = Column(Text)                                   # comma/newline separated
    experience_level = Column(String(30), default="Intermediate")  # Junior/Intermediate/Senior/Specialist
    availability = Column(String(50))                       # expected availability
    duration = Column(String(50))                           # expected participation period
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CompanyProject", backref="staffing_plan")

    def __repr__(self):
        return f"<StaffingPlanItem {self.position} x{self.count_required}>"


class ExpressionOfInterest(Base):
    __tablename__ = "expression_of_interests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(
        Integer, ForeignKey("company_projects.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    position = Column(String(120))                    # position the member wants
    skills = Column(Text)                             # skills they bring
    status = Column(String(20), default="pending", index=True)  # pending / selected / declined / withdrawn
    admin_notes = Column(Text)
    decided_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    decided_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CompanyProject", backref="expressions_of_interest")
    user = relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return f"<ExpressionOfInterest project={self.project_id} user={self.user_id} {self.status}>"


class ProjectChangeRequest(Base):
    __tablename__ = "project_change_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(
        Integer, ForeignKey("company_projects.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    reason = Column(Text)
    # Impact analysis fields (filled by admin/PM during review).
    impact_analysis = Column(Text)
    technical_review = Column(Text)
    cost_impact = Column(Numeric(14, 2))
    time_impact_days = Column(Integer)
    status = Column(String(30), default="pending", index=True)
    # pending / under_review / approved / declined / implemented
    decided_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    decided_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CompanyProject", backref="change_requests")
    requester = relationship("User", foreign_keys=[requested_by])

    def __repr__(self):
        return f"<ProjectChangeRequest {self.title} {self.status}>"
