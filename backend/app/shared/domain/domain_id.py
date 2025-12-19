"""Reusable Domain ID Value Object."""
from dataclasses import dataclass, field
from typing import Callable, Self
from uuid import UUID, uuid7


_UUID_FACTORY: Callable[[], UUID] = uuid7

@dataclass(frozen=True, slots=True)
class DomainID:
    """
    Base Value Object for all Entity IDs.
    Provides a unified way to handle UUIDv7 across the whole system.
    """

    value: UUID = field(default_factory=_UUID_FACTORY)

    @classmethod
    def from_str(cls, uuid_str: str) -> Self:
        return cls(value=UUID(uuid_str))

    def __str__(self) -> str:
        return str(self.value)