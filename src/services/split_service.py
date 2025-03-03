from datetime import datetime
from typing import Optional

from src.domain.exceptions.db_exceptions import RecordNotFoundError
from src.domain.models.split import Split
from src.domain.rep_interfaces.split_rep_interface import SplitRepInterface


class SplitService:
    def __init__(self, repository: SplitRepInterface) -> None:
        self.repository = repository

    async def create_split(self, data: Split) -> Split:
        return await self.repository.create(data)

    async def get_all_split(self) -> list[Optional[Split]]:
        object_instances = await self.repository.get_all()
        if object_instances == []:
            return []
        return [
            object_instance
            for object_instance in object_instances
            if object_instance
            if object_instance.deleted_at is None
        ]

    async def get_split_by_id(self, id: str) -> Optional[Split]:
        return await self.repository.get_by_id(id)

    async def update_split(self, id: str, data: Split) -> Split:
        data.updated_at = datetime.now()
        return await self.repository.update(id, data)

    async def delete_split(self, id: str) -> Split:
        object_instance = await self.repository.get_by_id(id)
        if object_instance is None:
            raise RecordNotFoundError('Split', id)
        object_instance.deleted_at = datetime.now()
        return await self.repository.update(id, object_instance)
