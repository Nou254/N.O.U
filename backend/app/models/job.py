"""
Job listing model.
"""

from sqlalchemy import Column, String, Text, DateTime, Date, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class JobListing(Base):
    __tablename__ = "job_listings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    department = Column(String(100))
    location = Column(String(100))
    employment_type = Column(String(50))
    requirements = Column(Text)
    salary_range = Column(String(100))
    status = Column(String(20), default="active")
    deadline = Column(Date)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    applications = relationship("Application", back_populates="job")
    
    def __repr__(self):
        return f"<JobListing {self.title}>"
