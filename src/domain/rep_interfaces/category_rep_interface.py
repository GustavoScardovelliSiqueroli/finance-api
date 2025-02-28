from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.category import Category


class CategoryRepInterface(ABC):
    @abstractmethod
    async def get_all(self) -> list[Optional[Category]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Category]:
        pass

    @abstractmethod
    async def create(self, data: Category) -> Category:
        pass

    @abstractmethod
    async def update(self, id: str, data: Category) -> Category:
        pass

    @abstractmethod
    async def delete(self, id: str) -> Category:
        pass
