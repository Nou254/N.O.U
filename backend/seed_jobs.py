"""
Seed job listings from the personnel categories & positions.

The careers page lists every job the admin manages. To make sure every
professional category in the admin appears as a career, this script creates
one job listing per personnel category (titled after the category) so the
public Careers section shows all the careers available in the admin.

Idempotent: existing listings are left untouched; missing ones are inserted.
Each listing carries a few positions from its category in the requirements.

Usage (from backend/):
    python seed_jobs.py
"""

import asyncio
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# Register the full model set so SQLAlchemy can resolve string-based
# relationships when mappers are configured in standalone scripts.
import app.models.project_release  # noqa: F401

from app.core.database import async_session_factory
from app.models.personnel import PersonnelCategory
from app.models.job import JobListing

# Map a category to the department shown on the careers page + job card.
def _department(name: str) -> str:
    name = name.lower()
    if "development" in name or "engineering" in name or "programming" in name:
        return "Engineering"
    if "design" in name or "media" in name or "marketing" in name:
        return "Design"
    if "database" in name or "data" in name or "cloud" in name or "devops" in name:
        return "Operations"
    if "documentation" in name or "knowledge" in name:
        return "Documentation"
    if "sales" in name or "business" in name or "finance" in name or "human" in name or "legal" in name:
        return "Operations"
    if "support" in name or "network" in name or "hardware" in name or "cctv" in name:
        return "Operations"
    if "internship" in name or "entry" in name or "general" in name:
        return "Engineering"
    return "Engineering"


async def seed() -> None:
    async with async_session_factory() as db:
        result = await db.execute(
            select(PersonnelCategory)
            .options(selectinload(PersonnelCategory.positions))
            .where(PersonnelCategory.is_active == "active")
            .order_by(PersonnelCategory.name)
        )
        categories = result.scalars().unique().all()

        added = 0
        for cat in categories:
            existing = await db.scalar(
                select(JobListing).where(JobListing.title == cat.name)
            )
            if existing:
                continue

            positions = [p.name for p in (cat.positions or [])]
            if len(positions) > 6:
                positions = positions[:6]
            req_lines = "\n".join(f"- {p}" for p in positions) if positions else "- Open to all levels"

            job = JobListing(
                title=cat.name,
                description=(
                    f"Join the {cat.name} team at N.O.U Digital Systems. "
                    f"{cat.description or 'Contribute your skills to real products and projects.'} "
                    "Apply with your names and email - no account needed - then take the "
                    "AI-powered assessment tailored to this career."
                ),
                department=_department(cat.name),
                location="Remote / Kisumu, Kenya",
                employment_type="full_time",
                requirements=req_lines,
                salary_range="Competitive",
                status="active",
            )
            db.add(job)
            added += 1

        await db.commit()
        print(f"Seeded {added} job listing(s) from {len(categories)} active career categories")


if __name__ == "__main__":
    asyncio.run(seed())
