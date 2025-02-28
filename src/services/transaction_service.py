from datetime import datetime
from typing import Any, Optional

from src.domain.models.transaction import Transaction
from src.domain.rep_interfaces.transaction_rep_interface import TransactionRepInterface
from src.services.category_service import CategoryService


class TransactionService:
    def __init__(
        self,
        repository: TransactionRepInterface,
        category_service: CategoryService,
    ) -> None:
        self.category_service = category_service
        self.repository = repository

    async def create_transaction(self, data: Transaction) -> Transaction:
        return await self.repository.create(data)

    async def get_all_transaction(self) -> list[Optional[Transaction]]:
        object_instances = await self.repository.get_all()
        if object_instances == []:
            return []
        return [
            object_instance
            for object_instance in object_instances
            if object_instance
            if object_instance.deleted_at is None
        ]

    async def get_transaction_by_id(self, id: str) -> Optional[Transaction]:
        return await self.repository.get_by_id(id)

    async def update_transaction(self, id: str, data: dict[str, Any]) -> Transaction:
        data['updated_at'] = datetime.now()
        return await self.repository.update(id, data)

    async def delete_transaction(self, id: str) -> Transaction:
        return await self.repository.update(id, {'deleted_at': datetime.now()})

    async def add_category(self, id: str, id_category: str) -> Transaction:
        return await self.repository.add_category(id, id_category)
