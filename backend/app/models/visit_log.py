"""
Site visit tracking.

Records one row per page view (public GET requests). Used by the admin
analytics report: daily visits, unique visitors (by IP), most-viewed pages.
"""

from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class SiteVisit(Base):
    __tablename__ = "site_visits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    visit_date = Column(Date, nullable=False, index=True)
    path = Column(String(255), nullable=False, index=True)
    ip = Column(String(64), index=True)
    user_agent = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<SiteVisit {self.visit_date} {self.path}>"
