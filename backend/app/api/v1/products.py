"""
Products API endpoints (public read + download).

Write operations (create/update/delete) are handled exclusively by the
admin router (/api/v1/admin/products) - the duplicate copies that previously
lived here were removed to reduce the attack surface (Pentest finding:
duplicate product endpoints).
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
import os

from app.core.database import get_db
from app.models.product import Product, ProductVersion

router = APIRouter()


def _product_payload(p: Product) -> dict:
    """Serialize a product for the public catalogue."""
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "category": p.category,
        "version": p.version,
        "status": p.status,
        "platforms": (p.platforms or "").split(",") if p.platforms else [],
        "licence": p.licence,
        "requirements": p.requirements,
        "features": p.features,
        "featured": bool(p.featured),
        "file_size": p.file_size,
        "download_count": p.download_count,
        "created_at": p.created_at,
    }


@router.get("/")
async def list_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    status: Optional[str] = None,
    platform: Optional[str] = None,
    featured: Optional[bool] = Query(None),
    sort: Optional[str] = Query(None, pattern="^(new)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    List all products with search + filters (category / status / platform /
    featured) matching the N.O.U. software catalogue (today.md Ch.5).
    """
    query = select(Product).where(Product.is_active == True)

    if category:
        query = query.where(Product.category == category)
    if search:
        like = f"%{search}%"
        query = query.where(
            (Product.name.ilike(like))
            | (Product.description.ilike(like))
            | (Product.category.ilike(like))
        )
    if status:
        query = query.where(Product.status == status)
    if platform:
        query = query.where(Product.platforms.ilike(f"%{platform}%"))
    if featured is not None:
        query = query.where(Product.featured == featured)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    query = query.order_by(
        Product.created_at.desc() if sort == "new" else Product.name.asc()
    )
    # Apply pagination
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()

    return {
        "products": [_product_payload(p) for p in products],
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    }


@router.get("/{product_id}")
async def get_product(
    product_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get product details with versions.
    """
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.is_active == True)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Get product versions
    versions_result = await db.execute(
        select(ProductVersion)
        .where(ProductVersion.product_id == product_id)
        .order_by(ProductVersion.released_at.desc())
    )
    versions = versions_result.scalars().all()

    return {
        "product": _product_payload(product),
        "versions": [{
            "id": v.id,
            "version_number": v.version_number,
            "release_notes": v.release_notes,
            "file_size": v.file_size,
            "is_latest": v.is_latest,
            "released_at": v.released_at,
        } for v in versions]
    }


@router.get("/{product_id}/download")
async def download_product(
    product_id: str,
    version_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Download product file (served as an attachment, never inline, so even a
    maliciously-uploaded file cannot execute in the browser - M2 hardening).
    """
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.is_active == True)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if not product.file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product file not available"
        )

    # Check if file exists
    if not os.path.exists(product.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product file not found on server"
        )

    # Increment download count
    product.download_count += 1
    await db.flush()

    # Return file
    filename = os.path.basename(product.file_path)
    return FileResponse(
        path=product.file_path,
        filename=filename,
        media_type="application/octet-stream",
        content_disposition_type="attachment",
    )
