"""Use case contract."""

from typing import Protocol, TypeVar

C = TypeVar("C", contravariant=True)
R = TypeVar("R", covariant=True)


class UseCase(Protocol[C, R]):
    """
    Generic application use case contract.

    A use case represents one application action (command/query) and exposes a
    single `execute(...)` method.
    """

    async def execute(self, command: C) -> R:
        """Execute the use case with the given command."""
        ...
