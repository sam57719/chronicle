"""Domain entities for the Items module."""

from dataclasses import dataclass, field
from .value_objects import ItemID


@dataclass(frozen=True, slots=True)
class Item:
    """
    Item entity.

    The ID is generated automatically using UUIDv7 (via ItemID),
    ensuring items are time-ordered in the database.
    """

    name: str
    description: str | None = None

    id: ItemID = field(default_factory=ItemID)

    def __post_init__(self) -> None:
        """Enforce domain invariants."""
        if not self.name.strip():
            raise ValueError("Item name cannot be empty")
