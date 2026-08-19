"""
User model.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    last_login = Column(DateTime)
    # Company handle used in the developer community and on projects
    # (displayed as @handle, e.g. @henrydatabase). Created by the user
    # themselves after their credentials are issued.
    username = Column(String(30), unique=True, nullable=True, index=True)
    # Contact details captured at application time (public apply form).
    phone = Column(String(30), nullable=True)
    # Stored CV file path (uploads/cvs/...) so HR/admin can download it.
    cv_file_path = Column(String(500), nullable=True)
    # AI (Groq) review of the applicant's CV, generated on admin request
    # (JSON: {summary, highlights, ...}) - shown in the admin HR screens.
    cv_summary = Column(Text, nullable=True)
    # The applicant's chosen place of qualification (professional category +
    # position). The assessment is built around this choice.
    qualification_category_id = Column(Integer, nullable=True)
    qualification_position_id = Column(Integer, nullable=True)
    qualification_category_name = Column(String(120), nullable=True)
    qualification_position_name = Column(String(120), nullable=True)
    # Terms & privacy agreement: set on registration and re-confirmed at
    # first login. Users cannot submit details until they have agreed.
    terms_accepted_at = Column(DateTime)
    # Organization policies agreement: approved personnel must review and
    # agree to the N.O.U. Organization Policies document on their first
    # login after approval (shown on the category screens too).
    policies_accepted_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="user", uselist=False)
    applications = relationship("Application", back_populates="applicant")
    assessment_sessions = relationship("AssessmentSession", back_populates="applicant")
    
    def __repr__(self):
        return f"<User {self.email}>"
