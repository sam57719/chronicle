"""Application services for the Items module."""

from app.shared.domain.ports import UnitOfWork
from ..domain.entities import Item
from ..domain.ports import ItemRepository
from ..domain.value_objects import ItemID


class ItemService:
    """
    Coordinates use cases for Items.

    This service is the 'brain' that the API or CLI will talk to.
    """

    def __init__(self, repository: ItemRepository, uow: UnitOfWork):
        """
        Initialise the service with a repository.

        The repository is an implementation of the ItemRepository interface,
        which defines the contract for interacting with item data.

        The uow is an implementation of the UnitOfWork interface,
        which defines the contract for managing transactions.
        """
        self.repository = repository
        self.uow = uow

    async def create_item(self, name: str, description: str | None = None) -> Item:
        """Create a new item."""
        async with self.uow:
            item = Item(name=name, description=description)
            await self.repository.add(item)

            return item

    async def get_item(self, item_id: ItemID) -> Item | None:
        """Retrieve a specific item."""
        return await self.repository.get_by_id(item_id)

    async def list_items(self) -> list[Item]:
        """View the entire collection of items."""
        return await self.repository.list_all()
