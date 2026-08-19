"""
Personnel categories and positions (today.md - PERSONNEL CATEGORIES).

Every N.O.U. applicant/personnel member has ONE primary professional category
and may hold multiple positions/specializations. Categories and positions are
managed by administrators and drive the 5-part assessment structure
(Common -> Category -> Position -> Practical -> Professional).
"""

from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PersonnelCategory(Base):
    __tablename__ = "personnel_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), unique=True, nullable=False, index=True)
    description = Column(Text)
    # Default assessment weights (percent) for this category - configurable
    # per category (today.md: "the weighting should be configurable").
    weight_logic = Column(Integer, default=15)
    weight_general = Column(Integer, default=5)
    weight_category = Column(Integer, default=25)
    weight_position = Column(Integer, default=25)
    weight_practical = Column(Integer, default=25)
    weight_professional = Column(Integer, default=5)
    is_active = Column(String(10), default="active")  # active / inactive
    created_at = Column(DateTime, server_default=func.now())

    positions = relationship(
        "PersonnelPosition", back_populates="category",
        cascade="all, delete-orphan", order_by="PersonnelPosition.name",
    )

    def __repr__(self):
        return f"<PersonnelCategory {self.name}>"


class PersonnelPosition(Base):
    __tablename__ = "personnel_positions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(
        Integer, ForeignKey("personnel_categories.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    name = Column(String(120), nullable=False)
    # Educational modules this position is assessed in (today.md assessment
    # framework: 8 modules per category). Stored as JSON list of module names.
    modules = Column(Text)
    is_active = Column(String(10), default="active")
    created_at = Column(DateTime, server_default=func.now())

    category = relationship("PersonnelCategory", back_populates="positions")

    def __repr__(self):
        return f"<PersonnelPosition {self.name}>"
