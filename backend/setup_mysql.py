"""
Setup MySQL database for N.O.U Digital Systems.

Creates the database (if it does not exist) and builds every table from
the application's SQLAlchemy ORM models, so the schema always matches
the code that runs against it.
"""

import asyncio
import sys

import pymysql
from sqlalchemy.engine import make_url

from app.core.config import settings
from app.core.database import engine, Base

# Import all model modules so their tables are registered on Base.metadata.
# These imports are intentional — they populate SQLAlchemy's metadata.
from app.models import application, assessment, customer, job  # noqa: F401
from app.models import product, project_request, question, support, user  # noqa: F401


def create_database() -> None:
    """
    Connect to the MySQL server and create the application database if missing.
    """
    url = make_url(settings.DATABASE_URL)
    connection = pymysql.connect(
        host=url.host or "localhost",
        user=url.username or "root",
        password=url.password or "",
        port=url.port or 3306,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{url.database}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        connection.commit()
        print(f"Database '{url.database}' created successfully!")
    finally:
        connection.close()


async def create_tables() -> None:
    """
    Create all tables defined by the ORM models.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("All tables created successfully!")


def main() -> None:
    try:
        create_database()
        asyncio.run(create_tables())
        print("\nDatabase setup complete!")
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
