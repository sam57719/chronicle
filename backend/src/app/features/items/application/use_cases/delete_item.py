"""Get Item use case."""

from dataclasses import dataclass

from app.features.items.application.interfaces.repository import ItemRepository
from app.shared.application.interfaces.use_case import UseCase
from app.shared.domain.ports import UnitOfWork

from ...domain.entities import Item
from ...domain.value_objects import ItemID


@dataclass(frozen=True, slots=True)
class DeleteItemCommand:
    """Input for retrieving an item."""

    item_id: ItemID


class DeleteItem(UseCase[DeleteItemCommand, Item | None]):
    """Use case: retrieve an existing Item by its ID."""

    def __init__(self, repository: ItemRepository, uow: UnitOfWork) -> None:
        """Initialise the use case with a repository and unit of work."""
        self._repository = repository
        self._uow = uow

    async def execute(self, command: DeleteItemCommand) -> Item | None:
        """Retrieve an item by its ID."""
        async with self._uow:
            item = await self._repository.delete_by_id(command.item_id)
            return item
