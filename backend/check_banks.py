import asyncio
from app.core.database import async_session_factory
from app.services.question_bank import bank_counts
from app.models.personnel import PersonnelCategory
from sqlalchemy import select

async def check():
    async with async_session_factory() as db:
        cats = await db.execute(select(PersonnelCategory).where(PersonnelCategory.is_active == 'active'))
        for cat in cats.scalars().all():
            counts = await bank_counts(db, cat.id)
            total = sum(counts.values())
            print(f"{cat.name}: {total}/100")
asyncio.run(check())