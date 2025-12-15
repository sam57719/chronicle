"""Service layer for handling Item objects."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.repositories.item_repo import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate, ItemRead


class ItemService:
    """Service layer handling business logic for Item objects."""

    def __init__(self, db: AsyncSession):
        """
        Initialise the service with a database session.

        Args:
            db (AsyncSession): The SQLAlchemy async session.
        """
        self.repo = ItemRepository(db)

    async def list_items(self) -> List[ItemRead]:
        """
        Retrieve all items and convert them to schema objects.

        Returns:
            List[ItemRead]: List of all items as Pydantic schemas.
        """
        items: list[Item] = list(await self.repo.list())
        return [ItemRead.model_validate(item) for item in items]

    async def get_item(self, item_id: int) -> Optional[ItemRead]:
        """
        Retrieve a single item by ID.

        Args:
            item_id (int): The ID of the item to retrieve.

        Returns:
            Optional[ItemRead]: Item schema if found, else None.
        """
        item: Optional[Item] = await self.repo.get(item_id)
        if item is None:
            return None
        return ItemRead.model_validate(item)

    async def create_item(self, data: ItemCreate) -> ItemRead:
        """
        Create a new item.

        Args:
            data (ItemCreate): Schema containing item data.

        Returns:
            ItemRead: The created item as a schema.
        """
        item: Item = await self.repo.create(data.model_dump())
        return ItemRead.model_validate(item)

    async def update_item(self, item_id: int, data: ItemUpdate) -> Optional[ItemRead]:
        """
        Update an existing item by ID.

        Args:
            item_id (int): The ID of the item to update.
            data (ItemUpdate): Schema containing fields to update.

        Returns:
            Optional[ItemRead]: Updated item as a schema if found, else None.
        """
        item: Optional[Item] = await self.repo.get(item_id)
        if item is None:
            return None
        updated_item: Item = await self.repo.update(
            item, data.model_dump(exclude_unset=True)
        )
        return ItemRead.model_validate(updated_item)

    async def delete_item(self, item_id: int) -> bool:
        """
        Delete an item by ID.

        Args:
            item_id (int): The ID of the item to delete.

        Returns:
            bool: True if the item was deleted, False if not found.
        """
        item: Optional[Item] = await self.repo.get(item_id)
        if item is None:
            return False
        await self.repo.delete(item)
        return True
