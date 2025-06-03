from abc import ABC, abstractmethod
from typing import Any, Optional, Sequence
from uuid import UUID

from src.domain.models.transaction import Transaction


class TransactionRepInterface(ABC):
    @abstractmethod
    async def get_all(self, id_user: UUID) -> Sequence[Transaction]:
        pass

    @abstractmethod
    async def get_by_id(
        self, id: int, id_user: UUID, load_categories: bool = False
    ) -> Optional[Transaction]:
        pass

    @abstractmethod
    async def create(self, data: Transaction) -> Transaction:
        pass

    @abstractmethod
    async def update(self, id: int, data: dict[str, Any], id_user: UUID) -> Transaction:
        pass

    @abstractmethod
    async def delete(self, id: int, id_user: UUID) -> Transaction:
        pass

    @abstractmethod
    async def add_category(self, id: int, id_category: str) -> Transaction:
        pass
