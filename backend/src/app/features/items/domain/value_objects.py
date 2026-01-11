"""Value Objects for Items."""

from dataclasses import dataclass

from app.shared.domain.value_objects import DomainID


@dataclass(frozen=True, slots=True, kw_only=True)
class ItemID(DomainID):
    """Value Object for Item IDs."""

    ...
