"""
Weekly project progress reports and developer help requests.

- ProjectProgressReport: the team leader submits a weekly progress report
  graded as a percentage so investors can see how a project is doing.
- ProjectHelpRequest: a developer uploads a document about their own project
  (or an external/private project) any time to ask the company for help.
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Numeric, ForeignKey, Date
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProjectProgressReport(Base):
    __tablename__ = "project_progress_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("company_projects.id", ondelete="CASCADE"), nullable=False)
    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    week_label = Column(String(50), nullable=False)   # e.g. "Week 12" or ISO date range
    percentage = Column(Numeric(5, 2), nullable=False)  # team-leader reported 0-100
    summary = Column(Text)
    # Admin grading: the official percentage (verified). Until an admin
    # grades the report, investors see the leader-reported value.
    admin_percentage = Column(Numeric(5, 2), nullable=True)
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    graded_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CompanyProject", back_populates="progress_reports")
    # Two FK paths to users (reported_by / graded_by) - each relationship must
    # name its column or the mapper cannot determine the join condition.
    reporter = relationship("User", foreign_keys=[reported_by])
    grader = relationship("User", foreign_keys=[graded_by])

    def __repr__(self):
        return f"<ProjectProgressReport project={self.project_id} {self.week_label} {self.percentage}%>"


class ProjectDeadlineExtension(Base):
    """Team request to extend a project deadline (max 4 weeks past the
    scheduled deadline). An admin must approve before the project can
    continue past its original deadline."""

    __tablename__ = "project_deadline_extensions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("company_projects.id", ondelete="CASCADE"), nullable=False)
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    requested_days = Column(Integer, nullable=False, default=7)  # max 28 (4 weeks)
    reason = Column(Text)
    status = Column(String(20), default="pending")  # pending / approved / denied
    decided_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    decided_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CompanyProject", back_populates="deadline_extensions")
    requester = relationship("User", foreign_keys=[requested_by])

    def __repr__(self):
        return f"<ProjectDeadlineExtension project={self.project_id} +{self.requested_days}d {self.status}>"


class ProjectHelpRequest(Base):
    __tablename__ = "project_help_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("company_projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    stored_path = Column(String(500), nullable=False)
    message = Column(Text)                      # what help they need
    status = Column(String(20), default="open")  # open / in_progress / resolved
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CompanyProject", back_populates="help_requests")
    requester = relationship("User")

    def __repr__(self):
        return f"<ProjectHelpRequest project={self.project_id} {self.filename} {self.status}>"
