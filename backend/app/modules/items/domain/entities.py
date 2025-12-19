"""Domain entities for the Items module."""

from dataclasses import dataclass
from app.shared.domain.domain_id import DomainID


@dataclass(frozen=True, slots=True)
class Item:
    """Item entity."""

    id: DomainID
    name: str
