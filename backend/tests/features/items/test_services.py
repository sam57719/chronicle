import pytest
from app.features.items.application.services import ItemService
from app.features.items.infrastructure.repositories import InMemoryItemRepository
from app.features.items.domain.value_objects import ItemID


@pytest.fixture
def item_service():
    """Provides a service instance with a clean in-memory repo for every test."""
    repo = InMemoryItemRepository()
    return ItemService(repo)


async def test_create_item_generates_id_and_persists(item_service):
    # Act
    item = await item_service.create_item(name="Test Item", description="A description")

    # Assert
    assert item.name == "Test Item"
    assert isinstance(item.id, ItemID)

    # Verify it's actually in the "database"
    retrieved = await item_service.get_item(item.id)
    assert retrieved == item


async def test_list_items_returns_all_created_items(item_service):
    await item_service.create_item(name="Item 1")
    await item_service.create_item(name="Item 2")

    items = await item_service.list_items()

    assert len(items) == 2
    assert {i.name for i in items} == {"Item 1", "Item 2"}


async def test_create_item_with_empty_name_raises_error(item_service):
    # This proves our Domain Invariants are working through the service
    with pytest.raises(ValueError, match="Item name cannot be empty"):
        await item_service.create_item(name="")
