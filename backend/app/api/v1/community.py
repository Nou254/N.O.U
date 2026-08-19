"""
N.O.U. Community Chat API.

The community is an open chat group: anyone - personnel or public visitors -
can post a message freely and it appears immediately (freedom of expression
and communication - no admin approval gate). Administrators can still remove
inappropriate content after the fact.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, Field
from typing import Optional

from app.core.database import get_db
from app.core.rate_limit import check_rate_limit
from app.core.security import (
    get_optional_user,
    require_admin,
    require_authenticated,
)
from app.models.user import User
from app.models.community_post import CommunityPost

router = APIRouter()

VALID_CATEGORIES = {
    "general", "announcement", "question", "idea", "project",
    "help", "learning", "other",
}


def _post_payload(p: CommunityPost) -> dict:
    author_name = ""
    author_email = None
    author_username = None
    if p.author:
        author_name = f"{p.author.first_name} {p.author.last_name}".strip()
        author_email = p.author.email
        author_username = p.author.username
    if not author_name and p.guest_name:
        author_name = p.guest_name
    if not author_email and p.guest_email:
        author_email = p.guest_email
    return {
        "id": p.id,
        "author": {
            "id": p.author_id,
            "name": author_name or "Community Member",
            "email": author_email,
            "username": author_username,
        },
        "category": p.category,
        "department": p.department,
        "title": p.title,
        "content": p.content,
        "status": p.status,
        "removed_reason": p.removed_reason,
        "created_at": p.created_at,
        "updated_at": p.updated_at,
    }


class PostCreate(BaseModel):
    # Chat messages don't need a title (it is auto-derived from the message);
    # the developer/admin post forms still send one.
    title: Optional[str] = Field(None, max_length=255)
    content: str = Field(min_length=1, max_length=20000)
    category: str = Field("general", max_length=50)
    department: Optional[str] = Field(None, max_length=120)
    # Public chat visitors identify by display name (+ optional email) so the
    # community stays open to everyone (no login required).
    guest_name: Optional[str] = Field(None, max_length=120)
    guest_email: Optional[str] = Field(None, max_length=255)


class PostModeration(BaseModel):
    approve: bool = True
    reason: Optional[str] = None


@router.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(
    body: PostCreate,
    request: Request,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a community chat message. The community is open to everyone -
    no login required and no approval gate (freedom of expression). Every
    message is published immediately; administrators may remove content
    after the fact if it violates community guidelines."""
    if current_user is None:
        check_rate_limit(request, "community-chat:ip", max_hits=30, window_seconds=3600)

    if body.category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=422,
            detail=f"Category must be one of: {', '.join(sorted(VALID_CATEGORIES))}",
        )

    content = (body.content or "").strip()
    if not content:
        raise HTTPException(status_code=422, detail="Message cannot be empty")

    # Guests must identify with a display name so the community stays
    # accountable; registered users are identified by their account.
    guest_name = None
    guest_email = None
    if current_user is None:
        guest_name = (body.guest_name or "").strip()
        if len(guest_name) < 2:
            raise HTTPException(
                status_code=422,
                detail="Please enter your name to post in the community chat",
            )
        guest_email = (body.guest_email or "").strip() or None

    # Validate the department against the active personnel categories so only
    # real departments get their own community space.
    department = (body.department or "").strip() or None
    if department:
        from app.models.personnel import PersonnelCategory
        cat = await db.scalar(
            select(PersonnelCategory).where(PersonnelCategory.name == department)
        )
        if not cat or cat.is_active != "active":
            raise HTTPException(
                status_code=422,
                detail="Department must be an active professional category",
            )

    title = (body.title or "").strip()
    if not title:
        # Chat messages have no title - derive a short one for the feed.
        title = content[:60] + ("..." if len(content) > 60 else "")

    post = CommunityPost(
        author_id=current_user.id if current_user else None,
        guest_name=guest_name,
        guest_email=guest_email,
        category=body.category,
        department=department,
        title=title,
        content=content,
        # Published immediately - no admin approval gate.
        status="published",
    )
    db.add(post)
    await db.flush()
    await db.refresh(post)
    # Commit before responding so the new post is immediately visible to
    # subsequent reads (read-your-writes - same pattern as the investor and
    # recruit endpoints).
    await db.commit()
    await db.refresh(post)
    return {
        "message": "Message published",
        "post": _post_payload(post),
    }


@router.get("/posts")
async def list_posts(
    category: Optional[str] = None,
    department: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Community chat feed - public, no login required (freedom of
    expression). All messages are published immediately, so everyone sees
    the full conversation. Filterable by post category and/or department."""
    query = select(CommunityPost).where(CommunityPost.status == "published")
    if category:
        query = query.where(CommunityPost.category == category)
    if department:
        query = query.where(CommunityPost.department == department)
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(
        query.order_by(CommunityPost.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    return {
        "posts": [_post_payload(p) for p in result.scalars().all()],
        "categories": sorted(VALID_CATEGORIES),
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit if total else 0,
        },
    }


@router.get("/members")
async def department_members(
    department: str = Query(..., min_length=2, max_length=120),
    current_user: User = Depends(require_authenticated),
    db: AsyncSession = Depends(get_db),
):
    """Developers (and admins) belonging to a department community. Used by
    the department screens to show who is in the same team. Only personnel
    whose place of qualification matches the department are included."""
    from app.models.user import User
    result = await db.execute(
        select(User).where(
            User.role.in_(["developer", "admin"]),
            User.is_active.is_(True),
            User.qualification_category_name == department,
        ).order_by(User.first_name)
    )
    members = []
    for u in result.scalars().all():
        members.append({
            "id": u.id,
            "name": f"{u.first_name} {u.last_name}".strip() or u.email,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "qualification_category_name": u.qualification_category_name,
            "qualification_position_name": u.qualification_position_name,
        })
    return {"department": department, "members": members}


@router.get("/moderation")
async def moderation_queue(
    status_filter: Optional[str] = Query("pending"),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Administrative moderation queue (pending / published / removed)."""
    query = select(CommunityPost)
    if status_filter in ("pending", "published", "removed"):
        query = query.where(CommunityPost.status == status_filter)
    result = await db.execute(
        query.order_by(CommunityPost.created_at.desc())
    )
    return {"posts": [_post_payload(p) for p in result.scalars().all()]}


@router.post("/posts/{post_id}/moderate")
async def moderate_post(
    post_id: str,
    body: PostModeration,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Approve or remove a community post. Approval is no longer required for
    publication (all posts publish instantly), so this endpoint is used to
    remove content that violates community guidelines."""
    post = await db.scalar(
        select(CommunityPost).where(CommunityPost.id == post_id)
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if body.approve:
        post.status = "published"
        post.removed_reason = None
    else:
        post.status = "removed"
        post.removed_reason = body.reason or "Removed by N.O.U. administration"
    post.moderated_by = current_user.id
    post.moderated_at = func.now()
    await db.commit()
    await db.refresh(post)
    return {
        "message": "Post published" if body.approve else "Post removed",
        "post": _post_payload(post),
    }


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Authors delete their own posts; admins may delete any post. Guests
    (no account) cannot delete - administrators moderate their messages."""
    post = await db.scalar(
        select(CommunityPost).where(CommunityPost.id == post_id)
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if current_user is None or (
        post.author_id != current_user.id and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own posts",
        )
    await db.delete(post)
    await db.commit()
    return None
