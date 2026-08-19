"""
Organization policies document model.

Holds the single master policies document (N.O.U. Organization Policies) so
it can be shown on the admin category screens (after approval, for future
reference) and presented to approved personnel on their first login, where
they must agree to it before using the platform.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql import func

from app.core.database import Base


class SitePolicy(Base):
    __tablename__ = "site_policies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, default="N.O.U. Organization Policies")
    # Full policies document text (chapters 1-14 of the master document).
    # LONGTEXT on MySQL so the full 300K+ character document fits.
    content = Column(Text().with_variant(LONGTEXT(), "mysql"), nullable=False)
    version = Column(String(20), nullable=False, default="1.0")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<SitePolicy {self.title} v{self.version}>"
