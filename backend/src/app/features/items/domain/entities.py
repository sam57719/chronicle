"""Domain entities for the Items module."""

from dataclasses import dataclass, field
from typing import Self

from app.shared.domain.ports import DomainEntity

from .value_objects import ItemID


@dataclass(frozen=True, slots=True, kw_only=True)
class Item(DomainEntity):
    """
    Item entity.

    The ID is generated automatically using UUIDv7 (via ItemID),
    ensuring items are time-ordered in the database.
    """

    name: str
    description: str | None = None

    id: ItemID = field(default_factory=ItemID.create)

    def __post_init__(self) -> None:
        """Enforce domain invariants."""
        if not self.name.strip():
            raise ValueError("Item name cannot be empty")

    @classmethod
    def create(  # type: ignore[override]
        cls,
        *,
        name: str,
        description: str | None = None,
    ) -> Self:
        """Factory method to create a new Item with a generated ID."""
        return cls(name=name, description=description)

    # noinspection PyMethodOverriding
    @classmethod
    def load(  # type: ignore[override]
        cls,
        *,
        id_: ItemID,
        name: str,
        description: str | None = None,
    ) -> Self:
        """Factory method to load an existing Item."""
        return cls(id=id_, name=name, description=description)
