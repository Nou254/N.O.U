"""
Customer model.
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    company_name = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="customer")
    project_requests = relationship("ProjectRequest", back_populates="customer")
    support_tickets = relationship("SupportTicket", back_populates="customer")
    
    def __repr__(self):
        return f"<Customer {self.company_name or self.user.email}>"
