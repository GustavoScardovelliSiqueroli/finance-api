from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.split import Split


class SplitRepInterface(ABC):
    @abstractmethod
    async def get_all(self) -> list[Optional[Split]]:
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
