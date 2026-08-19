"""
Support ticket model.
"""

from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class SupportTicket(Base):
    __tablename__ = "support_tickets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    ticket_number = Column(Integer, autoincrement=True)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50))
    priority = Column(String(20), default="medium")
    status = Column(String(20), default="open")
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    resolved_at = Column(DateTime)
    
    # Relationships
    customer = relationship("Customer", back_populates="support_tickets")
    assignee = relationship("User", foreign_keys=[assigned_to])
    
    def __repr__(self):
        return f"<SupportTicket {self.ticket_number}>"
