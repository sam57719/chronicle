"""Database configuration and session helpers."""

from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from .config import settings
from contextlib import asynccontextmanager


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # True in dev if you want SQL logs
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    """Provide a transactional scope around a series of operations."""
    async with AsyncSessionLocal() as session:
        yield session
