import pytest

from app.features.items.application.use_cases.create_item import (
    CreateItem,
    CreateItemCommand,
)
from app.features.items.application.use_cases.get_item import GetItem, GetItemQuery
from app.features.items.application.use_cases.list_items import (
    ListItems,
    ListItemsQuery,
)
from app.features.items.domain.value_objects import ItemID
from app.features.items.persistence.in_memory_repository import InMemoryItemRepository
from app.shared.infrastructure.unit_of_work import InMemoryUnitOfWork


@pytest.fixture
def repo() -> InMemoryItemRepository:
    return InMemoryItemRepository()


@pytest.fixture
def uow() -> InMemoryUnitOfWork:
    return InMemoryUnitOfWork()


@pytest.fixture
def create_item_uc(repo: InMemoryItemRepository, uow: InMemoryUnitOfWork) -> CreateItem:
    return CreateItem(repository=repo, uow=uow)


@pytest.fixture
def get_item_uc(repo: InMemoryItemRepository, uow: InMemoryUnitOfWork) -> GetItem:
    return GetItem(repository=repo, uow=uow)


@pytest.fixture
def list_items_uc(repo: InMemoryItemRepository, uow: InMemoryUnitOfWork) -> ListItems:
    return ListItems(repository=repo, uow=uow)


async def test_create_item_persists_and_generates_id(
    create_item_uc: CreateItem,
    get_item_uc: GetItem,
) -> None:
    item = await create_item_uc.execute(
        CreateItemCommand(name="Test Item", description="A description")
    )

    assert item.name == "Test Item"
    assert isinstance(item.id, ItemID)

    retrieved = await get_item_uc.execute(GetItemQuery(item_id=item.id))
    assert retrieved == item


async def test_create_item_with_empty_name_raises_error(
    create_item_uc: CreateItem,
) -> None:
    with pytest.raises(ValueError, match="Item name cannot be empty"):
        await create_item_uc.execute(CreateItemCommand(name=""))


async def test_list_items_returns_all_created_items(
    create_item_uc: CreateItem,
    list_items_uc: ListItems,
) -> None:
    await create_item_uc.execute(CreateItemCommand(name="Item 1"))
    await create_item_uc.execute(CreateItemCommand(name="Item 2"))

    items = await list_items_uc.execute(ListItemsQuery())

    assert {i.name for i in items} == {"Item 1", "Item 2"}
