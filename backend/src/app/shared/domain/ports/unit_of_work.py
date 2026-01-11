"""Shared domain ports."""

from abc import ABC, abstractmethod
from typing import Self


class UnitOfWork(ABC):
    """
    Port for managing transactions.

    Used as an async context manager: 'async with <uow>'
    """

    def __init__(self) -> None:
        """Initialise the unit of work."""
        self._committed: bool = False

    async def __aenter__(self) -> Self:
        """Begin a transaction."""
        self._committed = False
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        """Commit or rollback the transaction."""
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self) -> None:
        """Persist all changes made during the transaction."""
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Discard all changes made during the transaction."""
        ...
