from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.user import User


class UserRepInterface(ABC):
    @abstractmethod
    async def get_all(self) -> list[Optional[User]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create(self, data: User) -> User:
        pass

    @abstractmethod
    async def update(self, id: str, data: User) -> User:
        pass

    @abstractmethod
    async def delete(self, id: str) -> User:
        pass
