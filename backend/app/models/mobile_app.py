"""
Mobile applications distributed through the N.O.U site.

Admins publish apps in two states:
- ``upcoming``  : announced with a banner + description, no download yet.
- ``published`` : the APK file is attached and customers can download it.

Anyone can view an app and leave a public comment (freedom of expression -
comments are never moderated before they appear).
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class MobileApp(Base):
    __tablename__ = "mobile_apps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    tagline = Column(String(255))
    description = Column(Text)
    version = Column(String(30), default="1.0.0")
    platform = Column(String(60), default="Android")
    # upcoming / published
    status = Column(String(20), default="upcoming", index=True)
    banner_image = Column(String(500))          # stored banner file path
    apk_file = Column(String(500))              # stored .apk file path
    apk_filename = Column(String(255))          # original filename for download
    apk_size = Column(Integer)                  # bytes
    downloads = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    creator = relationship("User")
    comments = relationship(
        "AppComment",
        back_populates="app",
        cascade="all, delete-orphan",
        order_by="AppComment.created_at",
    )

    def __repr__(self):
        return f"<MobileApp {self.id} {self.name} [{self.status}]>"


class AppComment(Base):
    __tablename__ = "app_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer, ForeignKey("mobile_apps.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255))
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    app = relationship("MobileApp", back_populates="comments")

    def __repr__(self):
        return f"<AppComment {self.id} on app {self.app_id}>"
