"""Repository for managing Item objects in the database."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Sequence

from app.models.item import Item


class ItemRepository:
    """Repository for performing CRUD operations on Item objects."""

    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with an async database session.

        Args:
            db (AsyncSession): The SQLAlchemy async session.
        """
        self.db = db

    async def list(self) -> Sequence[Item]:
        """
        Retrieve all items from the database.

        Returns:
            Sequence[Item]: A sequence of Item instances.
        """
        result = await self.db.execute(select(Item))
        return result.scalars().all()

    async def get(self, item_id: int) -> Optional[Item]:
        """
        Retrieve a single item by its ID.

        Args:
            item_id (int): The ID of the item to retrieve.

        Returns:
            Optional[Item]: The Item instance if found, else None.
        """
        result = await self.db.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> Item:
        """
        Create a new item in the database.

        Args:
            data (dict): A dictionary of fields for the new item.

        Returns:
            Item: The newly created Item instance.
        """
        item = Item(**data)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update(self, item: Item, data: dict) -> Item:
        """
        Update an existing item in the database.

        Args:
            item (Item): The item instance to update.
            data (dict): A dictionary of fields to update.

        Returns:
            Item: The updated Item instance.
        """
        for k, v in data.items():
            setattr(item, k, v)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete(self, item: Item) -> None:
        """
        Delete an item from the database.

        Args:
            item (Item): The item instance to delete.
        """
        await self.db.delete(item)
        await self.db.commit()
