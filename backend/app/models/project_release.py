"""
Software release model.

Admin uploads the *developed software* of a finished project (.apk, .zip,
.exe, .msi, .dmg, .ipa, .aab, ...) so customers can download it and install
it on their own devices. Releases belong to a CompanyProject and only become
publicly downloadable once the project is published.

The binary itself lives on disk under UPLOAD_DIR/projects/releases/; the row
stores metadata + the stored path. Downloads use the same short-lived
HMAC-signed URL mechanism as project documents (see projects_portal.py).
"""

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, BigInteger
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProjectRelease(Base):
    __tablename__ = "project_releases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(
        Integer, ForeignKey("company_projects.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    filename = Column(String(255), nullable=False)      # original file name, e.g. nou-app-v1.0.apk
    stored_path = Column(String(500), nullable=False)
    version = Column(String(40), default="1.0.0")       # release version tag
    platform = Column(String(60))                       # Android / Windows / Web / ...
    file_size = Column(BigInteger, default=0)
    downloads = Column(Integer, default=0)              # download counter
    is_active = Column(Boolean, default=True)           # soft delete
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    project = relationship("CompanyProject", back_populates="releases")
    uploader = relationship("User", foreign_keys=[uploaded_by])

    def __repr__(self):
        return f"<ProjectRelease {self.filename} v{self.version} ({self.platform})>"
