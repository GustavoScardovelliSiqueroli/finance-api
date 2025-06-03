from datetime import datetime
from typing import Optional, Sequence

from src.domain.models.split import Split
from src.domain.rep_interfaces.split_rep_interface import SplitRepInterface


class SplitService:
    def __init__(self, repository: SplitRepInterface) -> None:
        self.repository = repository

    async def create_splits(self, data: list[Split]) -> list[Split]:
        return await self.repository.create_many(data)

    async def get_all_split(self) -> Sequence[Split]:
        return await self.repository.get_all()

    async def get_split_by_id(self, id: str) -> Optional[Split]:
        return await self.repository.get_by_id(id)

    async def update_split(self, id: str, data: Split) -> Split:
        data.updated_at = datetime.now()
        return await self.repository.update(id, data)

    async def delete_split(self, id: str) -> Split:
        return await self.repository.delete(id)

    async def delete_all_split(self, id_transaction: int) -> Sequence[Split]:
        return await self.repository.delete_all(id_transaction)
