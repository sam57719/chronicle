"""Item domain ports."""

from typing import Protocol, runtime_checkable

from ...domain.entities import Item
from ...domain.value_objects import ItemID


@runtime_checkable
class ItemRepository(Protocol):
    """
    Port for Item storage.

    This is an interface. The Domain doesn't care if the data is
    stored in SQL, NoSQL, or a CSV file.
    """

    async def add(self, item: Item) -> None:
        """Save a new item to the collection."""
        ...

    async def get_by_id(self, item_id: ItemID) -> Item | None:
        """Retrieve an item by its unique Domain ID."""
        ...

    async def list_all(self) -> list[Item]:
        """Return all items in the collection."""
        ...
