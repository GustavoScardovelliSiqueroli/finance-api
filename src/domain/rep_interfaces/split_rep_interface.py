from abc import ABC, abstractmethod
from typing import Optional, Sequence

from src.domain.models.split import Split


class SplitRepInterface(ABC):
    @abstractmethod
    async def get_all(self) -> Sequence[Split]:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Split]:
        pass

    @abstractmethod
    async def create(self, data: Split) -> Split:
        pass

    @abstractmethod
    async def update(self, id: str, data: Split) -> Split:
        pass

    @abstractmethod
    async def delete(self, id: str) -> Split:
        pass

    @abstractmethod
    async def create_many(self, data: list[Split]) -> list[Split]:
        pass

    @abstractmethod
    async def delete_all(self, id_transaction: int) -> Sequence[Split]:
        pass
