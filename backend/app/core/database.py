"""
Database configuration and session management.
"""

import sys
import asyncio
import ssl
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# ---- Windows: switch to SelectorEventLoop (fixes SSL/WinError 87) ----
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ---- SSL configuration ----
# On Windows, we disable certificate verification for local development.
# On Linux (Render), we use full verification with certifi.
if sys.platform == "win32":
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
else:
    try:
        import certifi
        ca_certs = certifi.where()
    except ImportError:
        ca_certs = None
    ssl_context = ssl.create_default_context(cafile=ca_certs) if ca_certs else ssl.create_default_context()

connect_args = {
    "ssl": ssl_context
}

# ---- Create async engine ----
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args=connect_args,
)

# ---- Session factory ----
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """
    Base class for all database models.
    """
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session for dependency injection.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database tables.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Close database connections.
    """
    await engine.dispose()