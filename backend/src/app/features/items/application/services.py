"""Application services for the Items module."""

from ..domain.entities import Item
from ..domain.ports import ItemRepository
from ..domain.value_objects import ItemID


class ItemService:
    """
    Coordinates use cases for Items.

    This service is the 'brain' that the API or CLI will talk to.
    """

    def __init__(self, repository: ItemRepository):
        """
        Initialize the service with a repository.

        The repository is an implementation of the ItemRepository interface,
        which defines the contract for interacting with item data.
        """
        self.repository = repository

    def create_item(self, name: str, description: str | None = None) -> Item:
        """Create a new item."""
        # 1. Create the Domain Entity (it generates its own UUIDv7 ID)
        item = Item(name=name, description=description)

        # 2. Persist it using the repository
        self.repository.add(item)

        return item

    def get_item(self, item_id: ItemID) -> Item | None:
        """Retrieve a specific item."""
        return self.repository.get_by_id(item_id)

    def list_items(self) -> list[Item]:
        """View the entire collection of items."""
        return self.repository.list_all()
