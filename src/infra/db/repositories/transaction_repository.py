import re
from typing import Any, Optional, Sequence
from uuid import UUID

import aiomysql  # type: ignore
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from src.domain.exceptions.db_exceptions import (
    DuplicateRecordError,
    ForeignKeyError,
    RecordNotFoundError,
)
from src.domain.models.category import Category
from src.domain.models.transaction import Transaction
from src.domain.rep_interfaces.transaction_rep_interface import TransactionRepInterface
from src.infra.db.database import async_session


class TransactionRepository(TransactionRepInterface):
    def __init__(
        self, session: async_sessionmaker[AsyncSession] = async_session
    ) -> None:
        self.session = session

    async def get_all(self, id_user: UUID) -> Sequence[Transaction]:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Transaction).where(Transaction.id_user == id_user)
                result = await session.execute(stmt)
                return result.scalars().all()

    async def create(self, data: Transaction) -> Transaction:
        try:
            async with self.session() as session:
                async with session.begin():
                    session.add(data)
                await session.commit()
                await session.refresh(data)
                return data
        except IntegrityError as e:
            if isinstance(e.orig, aiomysql.Error) and e.orig.args[0] == 1062:
                error_message = e.orig.args[1]
                column_name = error_message.split("'")[3]
                raise DuplicateRecordError(
                    str(column_name), str(data.__dict__['column_name'])
                ) from e
            if isinstance(e.orig, aiomysql.MySQLError) and e.orig.args[0] == 1452:
                error_message = str(e.orig.args[1])
                match = re.search(
                    r'FOREIGN KEY \(`(.+?)`\) REFERENCES `(.+?)`', error_message
                )

                if match:
                    column_name = match.group(1)
                    table_name = match.group(2)
                else:
                    column_name = 'unknown_column'
                    table_name = 'unknown_table'

                raise ForeignKeyError(
                    table_name=table_name,
                    column_name=column_name,
                ) from e
            raise e

    async def get_by_id(
        self, id: int, id_user: UUID, load_categories: bool = False
    ) -> Optional[Transaction]:
        async with self.session() as session:
            async with session.begin():
                stmt = (
                    select(Transaction)
                    .where(Transaction.id == id)
                    .where(Transaction.id_user == id_user)
                )
                if load_categories:
                    stmt = stmt.options(selectinload(Transaction.categories))
                result = await session.execute(stmt)
                return result.scalars().first()

    async def update(self, id: int, data: dict[str, Any], id_user: UUID) -> Transaction:
        async with self.session() as session:
            async with session.begin():
                updatable_fields = {
                    k: v
                    for k, v in data.items()
                    if hasattr(Transaction, k) and k not in ('id', 'id_user')
                }

                if not updatable_fields:
                    raise ValueError('No valid fields to update')

                result = await session.execute(
                    update(Transaction)
                    .where(Transaction.id == id)
                    .where(Transaction.id_user == id_user)
                    .values(**updatable_fields)
                    .returning(Transaction)
                )

                updated = result.scalars().first()
                if not updated:
                    raise RecordNotFoundError('Transaction', str(id))

                return updated

    async def delete(self, id: int, id_user: UUID) -> Transaction:
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(
                    delete(Transaction)
                    .where(Transaction.id == id)
                    .where(Transaction.id_user == id_user)
                    .returning(Transaction)
                )
                object_instance = result.scalars().first()
                if not object_instance:
                    raise RecordNotFoundError('Transaction', str(id))
                return object_instance

    async def add_category(self, id: int, id_category: str) -> Transaction:
        async with self.session() as session:
            async with session.begin():
                stmt = (
                    select(Transaction)
                    .where(Transaction.id == id)
                    .options(selectinload(Transaction.categories))
                )
                result = await session.execute(stmt)
                transaction = result.scalars().first()

                if not transaction:
                    raise RecordNotFoundError('Transaction', str(id))

                category = await session.get(Category, id_category)

                if not category:
                    raise RecordNotFoundError('Category', id_category)

                transaction.categories.append(category)

                await session.commit()
                return transaction
