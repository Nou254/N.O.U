"""
Community post models.

Implements the N.O.U. Community (today.md - N.O.U. COMMUNITY POLICY): a
controlled communication and collaboration environment for approved
personnel. Posts carry a category, a moderation status and the author.
"""

from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Registered users link their message to their account. Public chat
    # visitors (freedom of expression) post with a display name + optional
    # email instead - author_id stays NULL for them.
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True
    )
    guest_name = Column(String(120), nullable=True)
    guest_email = Column(String(255), nullable=True)
    category = Column(String(50), default="general", index=True)
    # Department community the post belongs to (personnel category name).
    # NULL means the general community linking every department.
    department = Column(String(120), nullable=True, index=True)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    # pending / published / removed
    status = Column(String(20), default="pending", index=True)
    removed_reason = Column(String(255))
    moderated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    moderated_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    author = relationship("User", foreign_keys=[author_id], lazy="selectin")

    def __repr__(self):
        return f"<CommunityPost {self.title}>"
