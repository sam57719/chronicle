"""Value Objects for Items."""
from dataclasses import dataclass

from app.shared.domain.domain_id import DomainID

@dataclass(frozen=True, slots=True)
class ItemID(DomainID):
    """
    Value Object for Item IDs.
    """
    ...
