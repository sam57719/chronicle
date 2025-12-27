"""Dependency injection for the items module."""

from functools import lru_cache
from app.features.items.application.services import ItemService
from app.features.items.infrastructure.repositories import InMemoryItemRepository


@lru_cache
def get_item_repository() -> InMemoryItemRepository:
    """
    Returns a singleton instance of the repository.

    LRU Cache ensures we don't lose data between requests
    while using the In-Memory implementation.
    """
    return InMemoryItemRepository()


def get_item_service() -> ItemService:
    """Injects the repository into the service."""
    repo = get_item_repository()
    return ItemService(repo)
