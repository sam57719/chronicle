import pytest

from app.features.items.domain.entities import Item


def test_item_entity_creation() -> None:
    item = Item.create(name="Test Item", description="A test item for testing purposes")
    assert item.name == "Test Item"
    assert item.description == "A test item for testing purposes"
    assert item.id is not None


def test_item_entity_creation_with_empty_name_raises_error() -> None:
    with pytest.raises(ValueError, match="Item name cannot be empty"):
        Item.create(name="", description="A test item for testing purposes")


def test_item_entity_instantiation_with_invalid_id_raises_error() -> None:

    # noinspection PyTypeChecker
    Item(
        id="123",  # type: ignore[arg-type]
        name="Test Item",
        description="A test item for testing purposes",
    )


def test_item_entity_load_existing() -> None:
    item = Item.create(name="Test Item", description="A test item for testing purposes")
    loaded_item = Item.load(id_=item.id, name=item.name, description=item.description)
    assert loaded_item == item
