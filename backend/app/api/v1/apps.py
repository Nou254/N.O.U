"""
Public mobile-apps router.

Customers browse the apps N.O.U. publishes: published apps can be
downloaded (APK), upcoming apps are announced with a banner + description,
and anyone can leave a public comment on an app (published instantly -
freedom of expression).
"""

import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.mobile_app import MobileApp, AppComment
from app.services.email import send_email

router = APIRouter()

# Image types for banners (browsers report these reliably).
_BANNER_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
}


def _app_payload(a: MobileApp, with_comments: bool = False) -> dict:
    payload = {
        "id": a.id,
        "name": a.name,
        "tagline": a.tagline,
        "description": a.description,
        "version": a.version,
        "platform": a.platform,
        "status": a.status,
        "banner_url": f"/api/v1/apps/{a.id}/banner" if a.banner_image else None,
        "apk_filename": a.apk_filename,
        "apk_size": a.apk_size,
        "downloads": a.downloads or 0,
        "created_at": a.created_at,
        "comments_count": len(a.comments) if a.comments is not None else 0,
    }
    if with_comments:
        payload["comments"] = [
            {
                "id": c.id,
                "name": c.name,
                "comment": c.comment,
                "created_at": c.created_at,
            }
            for c in (a.comments or [])
        ]
    return payload


@router.get("/apps")
async def list_apps(db: AsyncSession = Depends(get_db)):
    """All active apps - published (downloadable) and upcoming (announced)."""
    rows = await db.execute(
        select(MobileApp)
        .options(selectinload(MobileApp.comments))
        .where(MobileApp.is_active == True)  # noqa: E712
        .order_by(MobileApp.status.desc(), MobileApp.created_at.desc())
    )
    return {"apps": [_app_payload(a) for a in rows.scalars().all()]}


@router.get("/apps/{app_id}")
async def get_app(app_id: str, db: AsyncSession = Depends(get_db)):
    """One app with its full comment thread."""
    app = await db.scalar(
        select(MobileApp)
        .options(selectinload(MobileApp.comments))
        .where(MobileApp.id == app_id, MobileApp.is_active == True)  # noqa: E712
    )
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    return {"app": _app_payload(app, with_comments=True)}


@router.get("/apps/{app_id}/banner")
async def get_app_banner(app_id: str, db: AsyncSession = Depends(get_db)):
    """Serve the app's banner image (stored under uploads/apps/banners)."""
    app = await db.scalar(
        select(MobileApp).where(MobileApp.id == app_id, MobileApp.is_active == True)  # noqa: E712
    )
    if not app or not app.banner_image:
        raise HTTPException(status_code=404, detail="Banner not found")
    path = os.path.normpath(app.banner_image)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Banner file not found on the server")
    ext = os.path.splitext(path)[1].lower()
    media_type = _BANNER_TYPES.get(ext, "application/octet-stream")
    return FileResponse(path, media_type=media_type)


@router.get("/apps/{app_id}/download")
async def download_app(app_id: str, db: AsyncSession = Depends(get_db)):
    """Download the app's APK (published apps only)."""
    app = await db.scalar(
        select(MobileApp).where(MobileApp.id == app_id, MobileApp.is_active == True)  # noqa: E712
    )
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    if app.status != "published" or not app.apk_file:
        raise HTTPException(
            status_code=403,
            detail="This app is not available for download yet - it is coming soon.",
        )
    path = os.path.normpath(app.apk_file)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="APK file not found on the server")
    app.downloads = (app.downloads or 0) + 1
    await db.commit()
    return FileResponse(
        path,
        filename=app.apk_filename or os.path.basename(path),
        media_type="application/vnd.android.package-archive",
        content_disposition_type="attachment",
    )


class AppCommentIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: Optional[str] = Field(None, max_length=255)
    comment: str = Field(min_length=1, max_length=2000)


@router.post("/apps/{app_id}/comments", status_code=201)
async def add_app_comment(
    app_id: str,
    body: AppCommentIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Anyone can comment on an app - comments publish instantly (no approval)."""
    app = await db.scalar(
        select(MobileApp).where(MobileApp.id == app_id, MobileApp.is_active == True)  # noqa: E712
    )
    if not app:
        raise HTTPException(status_code=404, detail="App not found")

    comment = AppComment(
        app_id=app.id,
        name=body.name.strip(),
        email=body.email.strip() if body.email else None,
        comment=body.comment.strip(),
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    # Notify the N.O.U team quietly (non-blocking, dev-log fallback).
    try:
        await send_email(
            "noudigitalsystem@gmail.com",
            f"New comment on app: {app.name}",
            f"<p><b>{comment.name}</b> commented on <b>{app.name}</b>:</p>"
            f"<p>{comment.comment}</p>"
            f"<p><a href='http://localhost:3000/apps'>Open the Apps page</a></p>",
        )
    except Exception:  # noqa: BLE001 - notifications must never break comments
        pass

    return {
        "message": "Comment published",
        "comment": {
            "id": comment.id,
            "name": comment.name,
            "comment": comment.comment,
            "created_at": comment.created_at,
        },
    }
