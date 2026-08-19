"""
Product models.
"""

from sqlalchemy import Column, String, Text, Integer, BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False, index=True)
    version = Column(String(50), nullable=False)
    # N.O.U. product lifecycle status (today.md 5.10).
    status = Column(String(30), default="Available", server_default="Available", index=True)
    # Comma-separated platforms (today.md 5.9): Web, PWA, Android, Windows, ...
    platforms = Column(String(200), default="Web", server_default="Web")
    licence = Column(String(200))
    requirements = Column(Text)
    features = Column(Text)
    # Featured products shown on the home screen (today.md 5.13).
    featured = Column(Boolean, default=False, index=True)
    file_path = Column(String(500))
    file_size = Column(BigInteger)
    download_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    versions = relationship("ProductVersion", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product {self.name}>"


class ProductVersion(Base):
    __tablename__ = "product_versions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(String(50), nullable=False)
    release_notes = Column(Text)
    file_path = Column(String(500))
    file_size = Column(BigInteger)
    is_latest = Column(Boolean, default=True)
    released_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="versions")
    
    def __repr__(self):
        return f"<ProductVersion {self.version_number}>"
