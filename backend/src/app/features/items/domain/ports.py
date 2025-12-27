"""Item domain ports."""

from abc import ABC, abstractmethod
from .entities import Item
from .value_objects import ItemID


class ItemRepository(ABC):
    """
    Port for Item storage.

    This is an interface. The Domain doesn't care if the data is
    stored in SQL, NoSQL, or a CSV file.
    """

    @abstractmethod
    async def add(self, item: Item) -> None:
        """Save a new item to the collection."""
        ...

    @abstractmethod
    async def get_by_id(self, item_id: ItemID) -> Item | None:
        """Retrieve an item by its unique Domain ID."""
        ...

    @abstractmethod
    async def list_all(self) -> list[Item]:
        """Return all items in the collection."""
        ...
