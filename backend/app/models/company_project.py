"""
Company projects portal models.

Admin posts projects/jobs (with PDF/DOCX documentation). Developers join
projects subject to headcount rules; teams have a team leader and roles;
members chat and can call the AI for help; finished projects are uploaded
for admin review then published for customers.
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Date, Numeric
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class CompanyProject(Base):
    __tablename__ = "company_projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))            # e.g. network installation, web dev...
    required_people = Column(Integer, nullable=False, default=1)  # headcount needed
    status = Column(String(20), default="open")  # open / in_progress / review / completed / published
    # Full N.O.U. lifecycle stage (today.md PROJECT FLOW): the project moves
    # through controlled stages; developers only see opportunities once the
    # project reaches the staffing stage.
    lifecycle_stage = Column(
        String(40), default="requested", index=True,
        # requested / initial_review / clarification / analysis /
        # technical_feasibility / documentation / internal_review /
        # estimation / customer_proposal / customer_approval / staffing /
        # team_formation / planning / development / qa / security_review /
        # staging / customer_acceptance / deployment / support / closed /
        # on_hold / blocked / cancelled / rejected
    )
    team_leader_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    budget = Column(Numeric(12, 2))
    deadline = Column(Date)
    admin_notes = Column(Text)
    # Publish section for the customer gallery (Games, Bots, Education, ...).
    section = Column(String(50))
    # N.O.U. product classification (today.md): Free / Paid / Subscription /
    # Freemium / Enterprise / Custom / Internal.
    product_status = Column(String(40), default="Free", server_default="Free")
    # N.O.U. platform classification (today.md): Web / PWA / Android / ...
    platform = Column(String(60))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    team_leader = relationship("User", foreign_keys=[team_leader_id])
    creator = relationship("User", foreign_keys=[created_by])
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("ProjectDocument", back_populates="project", cascade="all, delete-orphan")
    # Downloadable software builds (.apk, .zip, ...) uploaded by the admin.
    releases = relationship(
        "ProjectRelease", back_populates="project",
        cascade="all, delete-orphan", order_by="ProjectRelease.created_at",
    )
    chat_messages = relationship("ProjectChatMessage", back_populates="project", cascade="all, delete-orphan")
    extra_requests = relationship("ExtraDeveloperRequest", back_populates="project", cascade="all, delete-orphan")
    progress_reports = relationship("ProjectProgressReport", back_populates="project", cascade="all, delete-orphan")
    help_requests = relationship("ProjectHelpRequest", back_populates="project", cascade="all, delete-orphan")
    deadline_extensions = relationship("ProjectDeadlineExtension", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CompanyProject {self.title} ({self.status})>"


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("company_projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(100))                 # e.g. database engineer (not restricted to one)
    is_team_leader = Column(Boolean, default=False)
    joined_at = Column(DateTime, server_default=func.now())

    project = relationship("CompanyProject", back_populates="members")
    user = relationship("User")

    def __repr__(self):
        return f"<ProjectMember project={self.project_id} user={self.user_id}>"


class ProjectDocument(Base):
    __tablename__ = "project_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("company_projects.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    stored_path = Column(String(500), nullable=False)
    doc_type = Column(String(30), default="spec")   # spec / completed / review / requirements / design / charter
    # Document approval workflow (today.md sec. 22): DRAFT -> UNDER REVIEW
    # -> REVISION REQUIRED -> RE-SUBMITTED -> APPROVED -> LOCKED VERSION.
    doc_status = Column(String(30), default="draft", index=True)
    version = Column(Integer, default=1)
    reviewer_notes = Column(Text)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CompanyProject", back_populates="documents")
    uploader = relationship("User", foreign_keys=[uploaded_by])

    def __repr__(self):
        return f"<ProjectDocument {self.filename} ({self.doc_type}) {self.doc_status}>"


class ProjectChatMessage(Base):
    __tablename__ = "project_chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("company_projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # None for AI messages
    message = Column(Text, nullable=False)
    is_ai = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CompanyProject", back_populates="chat_messages")
    user = relationship("User")

    def __repr__(self):
        return f"<ProjectChatMessage project={self.project_id} ai={self.is_ai}>"


class ExtraDeveloperRequest(Base):
    __tablename__ = "extra_developer_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("company_projects.id", ondelete="CASCADE"), nullable=False)
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    requested_count = Column(Integer, nullable=False, default=1)  # max 3
    reason = Column(Text)
    status = Column(String(20), default="pending")  # pending / approved / denied
    decided_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    decided_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CompanyProject", back_populates="extra_requests")
    requester = relationship("User", foreign_keys=[requested_by])

    def __repr__(self):
        return f"<ExtraDeveloperRequest project={self.project_id} count={self.requested_count} {self.status}>"
