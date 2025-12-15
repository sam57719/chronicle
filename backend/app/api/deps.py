"""Dependency injection for the API routes."""

from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import session_scope


async def get_async_db_session() -> AsyncIterator[AsyncSession]:
    """Yield an async SQLAlchemy session for request-scoped DB access."""
    async with session_scope() as session:
        yield session
