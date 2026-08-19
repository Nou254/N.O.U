"""
Company announcements (the "quorum" space).

Admins post jokes of the day, quotes, notices, or any communication for
developers and/or customers. Announcements appear in the role-scoped feeds on
the portal/customer dashboards; admins can also broadcast an email to all
customers (e.g. maintenance windows or incoming services).
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(Text, nullable=False)
    title = Column(String(255))
    # joke / quote / notice / update
    category = Column(String(30), default="update")
    # developers / customers / all
    audience = Column(String(20), default="all")
    pinned = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    creator = relationship("User")

    def __repr__(self):
        return f"<Announcement {self.id} [{self.category}] -> {self.audience}>"
