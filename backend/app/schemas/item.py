"""Item schema module."""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class ItemBase(BaseModel):
    """Base item schema."""

    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Item create schema."""

    pass


class ItemUpdate(BaseModel):
    """Item update schema."""

    name: Optional[str] = None
    description: Optional[str] = None


class ItemRead(ItemBase):
    """Item read schema."""

    id: int

    model_config = ConfigDict(from_attributes=True)
