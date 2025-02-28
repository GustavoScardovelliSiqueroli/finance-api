from datetime import datetime
from typing import Optional

from src.domain.exceptions.db_exceptions import RecordNotFoundError
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

    async def update_transaction(self, id: str, data: Transaction) -> Transaction:
        data.updated_at = datetime.now()
        return await self.repository.update(id, data)

    async def delete_transaction(self, id: str) -> Transaction:
        object_instance = await self.repository.get_by_id(id)
        if object_instance is None:
            raise RecordNotFoundError(id)
        object_instance.deleted_at = datetime.now()
        return await self.repository.update(id, object_instance)

    async def add_category(self, id: str, category_id: str) -> Transaction:
        transaction = await self.repository.get_by_id(id)
        if transaction is None:
            raise RecordNotFoundError(id)
        categoty = await self.category_service.get_category_by_id(category_id)
        if categoty is None:
            raise RecordNotFoundError(category_id)
        transaction.categories.append(categoty)
        return await self.repository.update(id, transaction)
