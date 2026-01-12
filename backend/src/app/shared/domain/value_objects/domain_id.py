"""Reusable Domain ID Value Object."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Self
from uuid import UUID, uuid7

from app.shared.domain.exceptions import InvalidDomainId
from app.shared.domain.ports import ValueObject

_UUID_FACTORY: Callable[[], UUID] = uuid7


@dataclass(frozen=True, slots=True)
class DomainID(ValueObject[UUID]):
    """
    Base Value Object for all Entity IDs.

    Provides a unified way to handle UUIDv7 across the whole system.
    """

    value: UUID = field(default_factory=_UUID_FACTORY)

    @classmethod
    def create(cls, value: UUID | str | None = None) -> Self:
        """
        Unified factory for Domain IDs.

        Accepts a UUID, a string representation, or None (to generate new).
        """
        if value is None:
            return cls()

        if isinstance(value, UUID):
            return cls(value=value)

        if isinstance(value, str):
            try:
                return cls(value=UUID(value))
            except ValueError:
                raise InvalidDomainId(id_class=cls, value=value)

        # Fallback for completely wrong types passed to .create()
        raise InvalidDomainId(
            id_class=cls,
            value=value,
            message=f"Invalid {cls.__name__}: "
            f"expected UUID or str, got {type(value).__name__}.",
        )

    def __post_init__(self) -> None:
        """Strict type validation for the raw value."""
        if not isinstance(self.value, UUID):
            raise InvalidDomainId(
                id_class=type(self),
                value=self.value,
                message=f"Invalid {type(self).__name__}: "
                f"expected UUID type, got {type(self.value).__name__}.",
            )
