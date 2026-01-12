"""Base class for domain entities."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from app.shared.domain import DomainID


class DomainEntity(ABC):
    """
    Base class for all domain entities.

    Enforces the factory pattern:
    - .create(): For new instances (business logic/validation).
    - .load(): For existing data (reconstructing from the database).
    """

    @property
    @abstractmethod
    def id(self) -> DomainID:
        """Identifier for the entity."""
        ...

    @classmethod
    @abstractmethod
    def create(cls, **kwargs: Any) -> Self:
        """Factory method to create a new instance of the entity."""
        ...

    @classmethod
    @abstractmethod
    def load(cls, *, id_: DomainID, **kwargs: Any) -> Self:
        """Factory method to load an existing instance of the entity."""
        ...
