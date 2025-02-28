from datetime import datetime
from typing import Optional

from src.domain.exceptions.db_exceptions import RecordNotFoundError
from src.domain.models.category import Category
from src.domain.rep_interfaces.category_rep_interface import CategoryRepInterface


class CategoryService:
    def __init__(self, repository: CategoryRepInterface) -> None:
        self.repository = repository

    async def create_category(self, data: Category) -> Category:
        return await self.repository.create(data)

    async def get_all_category(self) -> list[Optional[Category]]:
        object_instances = await self.repository.get_all()
        if object_instances == []:
            return []
        return [
            object_instance
            for object_instance in object_instances
            if object_instance
            if object_instance.deleted_at is None
        ]

    async def get_category_by_id(self, id: str) -> Optional[Category]:
        return await self.repository.get_by_id(id)

    async def update_category(self, id: str, data: Category) -> Category:
        data.updated_at = datetime.now()
        return await self.repository.update(id, data)

    async def delete_category(self, id: str) -> Category:
        object_instance = await self.repository.get_by_id(id)
        if object_instance is None:
            raise RecordNotFoundError('Category', id)
        object_instance.deleted_at = datetime.now()
        return await self.repository.update(id, object_instance)
