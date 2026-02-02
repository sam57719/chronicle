"""List Item use case."""

from dataclasses import dataclass

from app.features.items.application.interfaces.repository import ItemRepository
from app.shared.application.interfaces.use_case import UseCase
from app.shared.domain.ports import UnitOfWork

from ...domain.entities import Item


@dataclass(frozen=True, slots=True)
class ListItemsQuery:
    """Input for listing items."""


class ListItems(UseCase[ListItemsQuery, list[Item]]):
    """Use case: retrieve all existing Items."""

    def __init__(self, repository: ItemRepository, uow: UnitOfWork) -> None:
        """Initialise the use case with a repository and unit of work."""
        self._repository = repository
        self._uow = uow

    async def execute(self, command: ListItemsQuery) -> list[Item]:
        """Retrieve all items."""
        async with self._uow:
            items = await self._repository.list_all()
            return items
