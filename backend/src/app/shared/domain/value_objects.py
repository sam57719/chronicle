"""Reusable Domain ID Value Object."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Self
from uuid import UUID, uuid7

from app.shared.domain.exceptions import InvalidDomainId

_UUID_FACTORY: Callable[[], UUID] = uuid7


@dataclass(frozen=True, slots=True)
class DomainID:
    """
    Base Value Object for all Entity IDs.

    Provides a unified way to handle UUIDv7 across the whole system.
    """

    value: UUID = field(default_factory=_UUID_FACTORY)

    def __post_init__(self) -> None:
        """Validate the DomainID."""
        if not isinstance(self.value, UUID):
            raise InvalidDomainId(id_class=type(self), value=str(self.value))

    @classmethod
    def from_str(cls, uuid_str: str) -> Self:
        """
        Create a DomainID from a string.

        Catches invalid strings and raises our domain-specific exception.
        """
        try:
            return cls(value=UUID(uuid_str))
        except ValueError:
            raise InvalidDomainId(id_class=cls, value=uuid_str)

    def __str__(self) -> str:
        """Return a string representation of the DomainID."""
        return str(self.value)
