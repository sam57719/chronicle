"""Dependency injection for the items module."""

from functools import lru_cache

from fastapi import Depends

from app.entrypoints.api.dependencies import get_uow
from app.features.items.application.interfaces.repository import ItemRepository
from app.features.items.application.use_cases.create_item import CreateItem
from app.features.items.application.use_cases.get_item import GetItem
from app.features.items.application.use_cases.list_items import ListItems
from app.features.items.persistence.in_memory_repository import InMemoryItemRepository
from app.shared.domain.ports import UnitOfWork


@lru_cache
def get_item_repository() -> ItemRepository:
    """Provides a single instance of the ItemRepository."""
    return InMemoryItemRepository()


def get_create_item_use_case(
    repo: ItemRepository = Depends(get_item_repository),
    uow: UnitOfWork = Depends(get_uow),
) -> CreateItem:
    """Provides a use case instance with the given repository."""
    return CreateItem(repository=repo, uow=uow)


def get_get_item_use_case(
    repo: ItemRepository = Depends(get_item_repository),
    uow: UnitOfWork = Depends(get_uow),
) -> GetItem:
    """Provides a use case instance with the given repository."""
    return GetItem(repository=repo, uow=uow)


def get_list_items_use_case(
    repo: ItemRepository = Depends(get_item_repository),
    uow: UnitOfWork = Depends(get_uow),
) -> ListItems:
    """Provides a use case instance with the given repository."""
    return ListItems(repository=repo, uow=uow)
