"""
Complaint model.

Visitors / customers / applicants can file a complaint from the public
Complaints screen; every submission is forwarded to the administration for
review and resolution (status workflow: new -> in_progress -> resolved /
closed).
"""

from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(30))
    subject = Column(String(255), nullable=False)
    category = Column(String(60), default="General")
    message = Column(Text, nullable=False)
    status = Column(String(20), default="new")  # new / in_progress / resolved / closed
    admin_notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    resolved_at = Column(DateTime)

    def __repr__(self):
        return f"<Complaint {self.id} {self.subject}>"
