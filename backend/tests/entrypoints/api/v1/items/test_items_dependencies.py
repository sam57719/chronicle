from app.entrypoints.api.dependencies import get_uow
from app.entrypoints.api.v1.items.dependencies import (
    get_create_item_use_case,
    get_get_item_use_case,
    get_item_repository,
    get_list_items_use_case,
)
from app.features.items.application.use_cases.create_item import CreateItem
from app.features.items.application.use_cases.get_item import GetItem
from app.features.items.application.use_cases.list_items import ListItems
from app.features.items.persistence.in_memory_repository import InMemoryItemRepository
from app.shared.domain.ports import UnitOfWork


def test_get_item_repository_returns_in_memory_repo() -> None:
    repo = get_item_repository()
    assert isinstance(repo, InMemoryItemRepository)


def test_get_item_repository_is_singleton() -> None:
    repo1 = get_item_repository()
    repo2 = get_item_repository()

    assert repo1 is repo2


def test_uow_dependency_factory() -> None:
    uow = get_uow()
    assert isinstance(uow, UnitOfWork)


def test_create_item_usecase_dependency_factory() -> None:
    uc = get_create_item_use_case(repo=get_item_repository(), uow=get_uow())
    assert isinstance(uc, CreateItem)


def test_get_item_usecase_dependency_factory() -> None:
    uc = get_get_item_use_case(repo=get_item_repository(), uow=get_uow())
    assert isinstance(uc, GetItem)


def test_list_items_usecase_dependency_factory() -> None:
    uc = get_list_items_use_case(repo=get_item_repository(), uow=get_uow())
    assert isinstance(uc, ListItems)
