"""Dependency injection for the items module."""

from fastapi import Depends
from functools import lru_cache

from app.entrypoints.api.dependencies import get_uow
from app.features.items.application.services import ItemService
from app.features.items.infrastructure.repositories import InMemoryItemRepository
from app.shared.domain.ports import UnitOfWork


@lru_cache
def get_item_repository() -> InMemoryItemRepository:
    """Provides a single instance of the ItemRepository."""
    return InMemoryItemRepository()


def get_item_service(
    repo: InMemoryItemRepository = Depends(get_item_repository),
    uow: UnitOfWork = Depends(get_uow),
) -> ItemService:
    """Provides a service instance with the given repository."""
    return ItemService(repo, uow)
