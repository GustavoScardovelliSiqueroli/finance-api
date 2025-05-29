from datetime import datetime
from decimal import Decimal
from typing import Any, Optional, Sequence
from uuid import UUID

from src.domain.models.enums.type_enum import Type
from src.domain.models.split import Split
from src.domain.models.transaction import Transaction
from src.domain.rep_interfaces.transaction_rep_interface import TransactionRepInterface
from src.services.category_service import CategoryService
from src.services.split_service import SplitService


class TransactionService:
    def __init__(
        self,
        repository: TransactionRepInterface,
        category_service: CategoryService,
        split_service: SplitService,
    ) -> None:
        self.category_service = category_service
        self.repository = repository
        self.split_service = split_service

    async def create_transaction(self, data: Transaction) -> Transaction:
        return await self.repository.create(data)

    async def get_all_transaction(self, id_user: UUID) -> Sequence[Transaction]:
        object_instances = await self.repository.get_all(id_user)
        return object_instances

    async def get_transaction_by_id(
        self, id: str, id_user: UUID
    ) -> Optional[Transaction]:
        return await self.repository.get_by_id(id, id_user)

    async def update_transaction(
        self, id: str, data: dict[str, Any], id_user: UUID
    ) -> Transaction:
        data['updated_at'] = datetime.now()
        transaction = await self.repository.get_by_id(id, id_user)
        if transaction is None:
            raise ValueError(f'Transaction with ID {id} not found.')
        return await self.repository.update(id, data)

    async def delete_transaction(self, id: str, id_user: UUID) -> Transaction:
        transaction = await self.repository.get_by_id(id, id_user)
        if transaction is None:
            raise ValueError(f'Transaction with ID {id} not found.')
        return await self.repository.delete(id)

    async def add_category(self, id: str, id_category: str) -> Transaction:
        return await self.repository.add_category(id, id_category)

    async def remove_category(self, id: str, id_category: str) -> Transaction: ...

    async def add_splits(
        self, id: str, data: list[dict[str, Any]], id_user: UUID
    ) -> None:
        transaction = await self.repository.get_by_id(id, id_user)
        if transaction is None:
            raise ValueError(f'Transaction with ID {id} not found.')

        splits_sum = 0
        for split in data:
            splits_sum += split['value']
        if splits_sum != transaction.value:
            raise ValueError('Splits must add up to 100%')

        splits: list[dict[str, Any]] = []
        for split in data:
            category = await self.category_service.get_category_by_id(
                split['id_category']
            )
            if category is None:
                raise ValueError(f'Category with ID {split["category_id"]} not found.')

            if category.level != 1:
                raise ValueError(
                    f'Category with ID {split["category_id"]} is not level 1.'
                )
            split['id_transaction'] = id
            splits.append(split)

        for split in splits:
            split_model = Split(**split)
            await self.split_service.create_split(split_model)

        return

    async def remove_splits(self, id: str, id_split: str) -> Transaction:
        # REMOVE all splits
        ...

    async def get_balance(self, id_user: UUID) -> Decimal:
        balance: Decimal = Decimal('0')
        transactions = await self.get_all_transaction(id_user)
        for transaction in transactions:
            balance += (
                transaction.value
                if transaction.type == Type.INCOME
                else -transaction.value
            )

        return balance
