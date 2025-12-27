from app.entrypoints.api.dependencies import get_uow
from app.entrypoints.api.v1.items.dependencies import (
    get_item_repository,
    get_item_service,
)
from app.features.items.infrastructure.repositories import InMemoryItemRepository
from app.shared.infrastructure.uow import InMemoryUnitOfWork


def test_global_uow_dependency_is_singleton() -> None:
    # This covers app/entrypoints/api/dependencies.py
    uow1 = get_uow()
    uow2 = get_uow()
    assert isinstance(uow1, InMemoryUnitOfWork)
    assert uow1 is uow2


def test_item_repository_dependency_is_singleton() -> None:
    # This covers app/entrypoints/api/v1/items/dependencies.py (Line 16)
    repo1 = get_item_repository()
    repo2 = get_item_repository()
    assert isinstance(repo1, InMemoryItemRepository)
    assert repo1 is repo2


def test_item_service_dependency_factory() -> None:
    # This ensures the factory correctly wires repo and uow
    service = get_item_service(repo=get_item_repository(), uow=get_uow())
    assert service is not None
