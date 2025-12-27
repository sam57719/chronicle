"""Dependency injection for the items module."""

from fastapi import Depends
from functools import lru_cache
from app.features.items.application.services import ItemService
from app.features.items.infrastructure.repositories import InMemoryItemRepository


@lru_cache
def get_item_repository() -> InMemoryItemRepository:
    """Provides a single instance of the ItemRepository."""
    return InMemoryItemRepository()


def get_item_service(
    repo: InMemoryItemRepository = Depends(get_item_repository),
) -> ItemService:
    """Provides a service instance with the given repository."""
    return ItemService(repo)
