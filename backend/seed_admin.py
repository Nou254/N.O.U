"""
Seed the admin account if it does not exist.

Credentials are read ONLY from the environment (backend/.env) - never
hardcoded in source (pentest: hardcoded admin credentials were removed):

    NOU_ADMIN_EMAIL=admin@example.com
    NOU_ADMIN_PASSWORD=<strong password>

Run: python seed_admin.py
"""
import asyncio
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import select

# ---- Windows event-loop fix ----
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables from .env
load_dotenv()

from app.core.database import async_session_factory, init_db
from app.core.security import get_password_hash
from app.models.user import User


def _env_or_exit(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(
            f"Missing required environment variable {name} - set it in backend/.env "
            "before seeding the admin account."
        )
    return value


async def main() -> None:
    # ---- Ensure all tables exist ----
    print("Creating tables if they don't exist...")
    await init_db()
    print("Tables ready.")

    admin_email = _env_or_exit("NOU_ADMIN_EMAIL").lower()
    admin_password = _env_or_exit("NOU_ADMIN_PASSWORD")
    admin_first = os.environ.get("NOU_ADMIN_FIRST", "N.O.U")
    admin_last = os.environ.get("NOU_ADMIN_LAST", "Administrator")

    async with async_session_factory() as db:
        existing = await db.scalar(select(User).where(User.email == admin_email))
        if existing:
            print(f"admin already exists: {admin_email} (role={existing.role})")
            return
        admin = User(
            email=admin_email,
            password_hash=get_password_hash(admin_password),
            first_name=admin_first,
            last_name=admin_last,
            role="admin",
        )
        db.add(admin)
        await db.commit()
        print(f"admin created: {admin_email}")


if __name__ == "__main__":
    asyncio.run(main())