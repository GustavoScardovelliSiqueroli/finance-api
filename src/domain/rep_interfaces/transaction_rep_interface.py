from abc import ABC, abstractmethod
from typing import Any, Optional

from src.domain.models.transaction import Transaction


class TransactionRepInterface(ABC):
    @abstractmethod
    async def get_all(self) -> list[Optional[Transaction]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Transaction]:
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

    @abstractmethod
    async def get_transaction_values(self) -> list[float]:
        pass
