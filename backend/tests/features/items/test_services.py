import pytest

from app.features.items.application.services import ItemService
from app.features.items.domain.value_objects import ItemID
from app.features.items.infrastructure.repositories import InMemoryItemRepository
from app.shared.infrastructure.uow import InMemoryUnitOfWork


@pytest.fixture
def item_service() -> ItemService:
    """Provides a service instance with a clean in-memory repo for every test."""
    repo = InMemoryItemRepository()
    uow = InMemoryUnitOfWork()
    return ItemService(repo, uow)


async def test_create_item_generates_id_and_persists(item_service: ItemService) -> None:
    item = await item_service.create_item(name="Test Item", description="A description")

    assert item.name == "Test Item"
    assert isinstance(item.id, ItemID)

    retrieved = await item_service.get_item(item.id)
    assert retrieved == item


async def test_list_items_returns_all_created_items(item_service: ItemService) -> None:
    await item_service.create_item(name="Item 1")
    await item_service.create_item(name="Item 2")

    items = await item_service.list_items()

    assert len(items) == 2
    assert {i.name for i in items} == {"Item 1", "Item 2"}


async def test_create_item_with_empty_name_raises_error(
    item_service: ItemService,
) -> None:
    with pytest.raises(ValueError, match="Item name cannot be empty"):
        await item_service.create_item(name="")
