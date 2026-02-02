"""Create Item use case."""

from dataclasses import dataclass

from app.shared.application.interfaces.use_case import UseCase
from app.shared.domain.ports import UnitOfWork

from ...domain.entities import Item
from ...domain.ports import ItemRepository


@dataclass(frozen=True, slots=True)
class CreateItemCommand:
    """Input for creating an item."""

    name: str
    description: str | None = None


class CreateItem(UseCase[CreateItemCommand, Item]):
    """Use case: create a new Item and persist it within a transaction."""

    def __init__(self, repository: ItemRepository, uow: UnitOfWork) -> None:
        """Initialise the use case with a repository and unit of work."""
        self._repository = repository
        self._uow = uow

    async def execute(self, command: CreateItemCommand) -> Item:
        """Create a new item and persist it within a transaction."""
        async with self._uow:
            item = Item.create(name=command.name, description=command.description)
            await self._repository.add(item)
            return item
