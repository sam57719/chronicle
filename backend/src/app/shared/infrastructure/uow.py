"""Shared infrastructure implementations."""

from app.shared.domain.ports import UnitOfWork


class InMemoryUnitOfWork(UnitOfWork):
    """A no-op Unit of Work for in-memory testing/development."""

    async def commit(self) -> None:
        """Persist all changes made during the transaction."""
        self._committed = True
        pass

    async def rollback(self) -> None:
        """Discard all changes made during the transaction."""
        self._committed = False
        pass
