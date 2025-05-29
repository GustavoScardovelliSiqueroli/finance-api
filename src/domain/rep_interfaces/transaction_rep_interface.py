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
        self, id: str, id_user: UUID, load_categories: bool = False
    ) -> Optional[Transaction]:
        pass

    @abstractmethod
    async def create(self, data: Transaction) -> Transaction:
        pass

    @abstractmethod
    async def update(self, id: str, data: dict[str, Any]) -> Transaction:
        pass

    @abstractmethod
    async def delete(self, id: str) -> Transaction:
        pass

    @abstractmethod
    async def add_category(self, id: str, id_category: str) -> Transaction:
        pass
