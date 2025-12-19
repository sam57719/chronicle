"""Domain entities for the Items module."""
from dataclasses import dataclass
from typing import Callable
from uuid import UUID, uuid7
from app.shared.domain.domain_id import DomainID


@dataclass(frozen=True, slots=True)
class Item:
    id: DomainID
    name: str