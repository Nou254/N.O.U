"""
Application model.
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    applicant_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_listings.id", ondelete="CASCADE"), nullable=False)
    cover_letter = Column(Text)
    # Applicant's phone number captured on the public apply form.
    phone = Column(String(30))
    cv_file_path = Column(String(500))
    status = Column(String(20), default="submitted")
    admin_notes = Column(Text)
    submitted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    # Applicant's chosen place of qualification (category + position) - the
    # professional field they will be assessed in.
    category_id = Column(Integer, nullable=True)
    position_id = Column(Integer, nullable=True)
    category_name = Column(String(120), nullable=True)
    position_name = Column(String(120), nullable=True)
    
    # Relationships
    applicant = relationship("User", back_populates="applications")
    job = relationship("JobListing", back_populates="applications")
    
    def __repr__(self):
        return f"<Application {self.id}>"
