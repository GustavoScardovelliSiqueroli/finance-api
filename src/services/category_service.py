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
        datas = await self.repository.get_all()
        if datas == []:
            return []
        return [data for data in datas if data if data.deleted_at is None]

    async def get_category_by_id(self, id: str) -> Optional[Category]:
        return await self.repository.get_by_id(id)

    async def update_category(self, id: str, data: Category) -> Category:
        data.updated_at = datetime.now()
        return await self.repository.update(id, data)

    async def delete_category(self, id: str) -> Category:
        data = await self.repository.get_by_id(id)
        if data is None:
            raise RecordNotFoundError(id)
        data.deleted_at = datetime.now()
        return await self.repository.update(id, data)
