"""Item schemas for the API."""

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """Schema for creating a new Item."""

    name: str = Field(..., min_length=1)
    description: str | None = None


class ItemRead(BaseModel):
    """Schema for reading an existing Item."""

    id: str
    name: str
    description: str | None
