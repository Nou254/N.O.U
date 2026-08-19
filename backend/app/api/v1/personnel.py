"""
Personnel categories and positions API.

Today.md (PERSONNEL CATEGORIES): every applicant/personnel member has one
primary professional category plus optional positions/specializations. These
drive the 5-part assessment structure. Public/authenticated users can read;
only administrators create/edit/disable.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, Field
from typing import Optional, List
import json

from app.core.database import get_db
from app.core.security import get_optional_user, require_admin
from app.models.user import User
from app.models.personnel import PersonnelCategory, PersonnelPosition

router = APIRouter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class PositionIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    modules: Optional[str] = None
    is_active: Optional[str] = "active"


class CategoryIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: Optional[str] = None
    weight_logic: Optional[int] = 15
    weight_general: Optional[int] = 5
    weight_category: Optional[int] = 25
    weight_position: Optional[int] = 25
    weight_practical: Optional[int] = 25
    weight_professional: Optional[int] = 5
    positions: Optional[List[PositionIn]] = []
    is_active: Optional[str] = "active"


class CategoryUpdate(BaseModel):
    description: Optional[str] = None
    weight_logic: Optional[int] = None
    weight_general: Optional[int] = None
    weight_category: Optional[int] = None
    weight_position: Optional[int] = None
    weight_practical: Optional[int] = None
    weight_professional: Optional[int] = None
    is_active: Optional[str] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _position_payload(p: PersonnelPosition) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "modules": p.modules,
        "modules_list": json.loads(p.modules) if p.modules else [],
        "is_active": p.is_active,
    }


def _category_payload(c: PersonnelCategory, with_positions: bool = True) -> dict:
    payload = {
        "id": c.id,
        "name": c.name,
        "description": c.description,
        "weights": {
            "logic": c.weight_logic,
            "general": c.weight_general,
            "category": c.weight_category,
            "position": c.weight_position,
            "practical": c.weight_practical,
            "professional": c.weight_professional,
        },
        "is_active": c.is_active,
        "created_at": c.created_at,
    }
    if with_positions:
        payload["positions"] = [_position_payload(p) for p in (c.positions or [])]
    return payload


def _validate_weights(category: CategoryIn) -> None:
    total = (
        (category.weight_logic or 0)
        + (category.weight_general or 0)
        + (category.weight_category or 0)
        + (category.weight_position or 0)
        + (category.weight_practical or 0)
        + (category.weight_professional or 0)
    )
    if total != 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Assessment weights must total 100% (got {total}%)",
        )


# ---------------------------------------------------------------------------
# Public / authenticated reads
# ---------------------------------------------------------------------------
@router.get("/categories")
async def list_categories(
    include_inactive: bool = False,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """List personnel categories with their positions (public - no login)."""
    query = (
        select(PersonnelCategory)
        .options(selectinload(PersonnelCategory.positions))
    )
    if not include_inactive:
        query = query.where(PersonnelCategory.is_active == "active")
    result = await db.execute(query.order_by(PersonnelCategory.name))
    categories = result.scalars().unique().all()
    return {"categories": [_category_payload(c) for c in categories]}


@router.get("/categories/{category_id}")
async def get_category(
    category_id: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    category = await db.scalar(
        select(PersonnelCategory)
        .options(selectinload(PersonnelCategory.positions))
        .where(PersonnelCategory.id == category_id)
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return _category_payload(category)


@router.get("/positions")
async def list_positions(
    category_id: Optional[str] = None,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """List positions, optionally filtered by category (public - no login)."""
    query = select(PersonnelPosition)
    if category_id:
        query = query.where(PersonnelPosition.category_id == category_id)
    result = await db.execute(query.order_by(PersonnelPosition.name))
    positions = result.scalars().all()
    return {"positions": [_position_payload(p) for p in positions]}


# ---------------------------------------------------------------------------
# Admin management
# ---------------------------------------------------------------------------
@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(
    body: CategoryIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a professional category with optional positions."""
    _validate_weights(body)
    existing = await db.scalar(
        select(PersonnelCategory).where(PersonnelCategory.name == body.name)
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A category with this name already exists",
        )

    category = PersonnelCategory(
        name=body.name,
        description=body.description,
        weight_logic=body.weight_logic,
        weight_general=body.weight_general,
        weight_category=body.weight_category,
        weight_position=body.weight_position,
        weight_practical=body.weight_practical,
        weight_professional=body.weight_professional,
    )
    db.add(category)
    await db.flush()

    for pos in (body.positions or []):
        db.add(PersonnelPosition(
            category_id=category.id,
            name=pos.name,
            modules=pos.modules,
            is_active=pos.is_active or "active",
        ))

    await db.commit()
    fresh = await db.scalar(
        select(PersonnelCategory)
        .options(selectinload(PersonnelCategory.positions))
        .where(PersonnelCategory.id == category.id)
    )
    return _category_payload(fresh)


@router.put("/categories/{category_id}")
async def update_category(
    category_id: str,
    body: CategoryUpdate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    category = await db.scalar(
        select(PersonnelCategory).where(PersonnelCategory.id == category_id)
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Validate weights when provided.
    weights = {
        "weight_logic": body.weight_logic if body.weight_logic is not None else category.weight_logic,
        "weight_general": body.weight_general if body.weight_general is not None else category.weight_general,
        "weight_category": body.weight_category if body.weight_category is not None else category.weight_category,
        "weight_position": body.weight_position if body.weight_position is not None else category.weight_position,
        "weight_practical": body.weight_practical if body.weight_practical is not None else category.weight_practical,
        "weight_professional": body.weight_professional if body.weight_professional is not None else category.weight_professional,
    }
    total = sum(weights.values())
    if total != 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Assessment weights must total 100% (got {total}%)",
        )

    for field, value in weights.items():
        setattr(category, field, value)
    if body.description is not None:
        category.description = body.description
    if body.is_active is not None:
        category.is_active = body.is_active
    await db.commit()
    await db.refresh(category)
    return _category_payload(category)


@router.post("/categories/{category_id}/positions", status_code=status.HTTP_201_CREATED)
async def add_position(
    category_id: str,
    body: PositionIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    category = await db.scalar(
        select(PersonnelCategory).where(PersonnelCategory.id == category_id)
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    duplicate = await db.scalar(
        select(PersonnelPosition).where(
            PersonnelPosition.category_id == category_id,
            PersonnelPosition.name == body.name,
        )
    )
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A position with this name already exists in this category",
        )

    position = PersonnelPosition(
        category_id=category_id,
        name=body.name,
        modules=body.modules,
        is_active=body.is_active or "active",
    )
    db.add(position)
    await db.commit()
    await db.refresh(position)
    return _position_payload(position)


@router.put("/positions/{position_id}")
async def update_position(
    position_id: str,
    body: PositionIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    position = await db.scalar(
        select(PersonnelPosition).where(PersonnelPosition.id == position_id)
    )
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    position.name = body.name
    if body.modules is not None:
        position.modules = body.modules
    if body.is_active is not None:
        position.is_active = body.is_active
    await db.commit()
    await db.refresh(position)
    return _position_payload(position)
