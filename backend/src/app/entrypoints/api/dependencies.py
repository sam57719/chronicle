"""Dependency injection functions for the API."""

from functools import lru_cache

from app.shared.domain.ports import UnitOfWork
from app.shared.infrastructure.uow import InMemoryUnitOfWork


@lru_cache
def get_uow() -> UnitOfWork:
    """
    Provides a singleton instance of the UnitOfWork.

    Using lru_cache is essential for the InMemory version to ensure
    consistency across the request lifecycle.
    """
    return InMemoryUnitOfWork()
