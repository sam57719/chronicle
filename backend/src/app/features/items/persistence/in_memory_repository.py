"""Infrastructure implementations for Items."""

from app.features.items.application.interfaces.repository import ItemRepository
from app.features.items.domain.entities import Item
from app.features.items.domain.value_objects import ItemID


class InMemoryItemRepository(ItemRepository):
    """
    In-memory implementation of the ItemRepository.

    Useful for tests and local development without a database.
    """

    def __init__(self) -> None:
        """
        Initialise the in-memory repository.

        This constructor sets up an empty dictionary to store items,
        keyed by their ItemID.
        """
        self._items: dict[ItemID, Item] = {}

    async def add(self, item: Item) -> None:
        """Add an item to the in-memory store."""
        self._items[item.id] = item

    async def get_by_id(self, item_id: ItemID) -> Item | None:
        """Find an item by ID."""
        return self._items.get(item_id)

    async def list_all(self) -> list[Item]:
        """Return all stored items."""
        return list(self._items.values())
