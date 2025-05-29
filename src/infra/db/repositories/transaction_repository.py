import re
from typing import Any, Optional, Sequence
from uuid import UUID

import aiomysql  # type: ignore
from sqlalchemy import select
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
        self, id: str, id_user: UUID, load_categories: bool = False
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

    async def update(self, id: str, data: dict[str, Any]) -> Transaction:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Transaction).where(Transaction.id == id)
                result = await session.execute(stmt)
                object_instance = result.scalars().first()

                if not object_instance:
                    raise ValueError(f'Transaction with ID {id} not found.')

                for key, value in data.items():
                    if hasattr(object_instance, key) and key != 'id':
                        setattr(object_instance, key, value)

                session.add(object_instance)
                await session.commit()

                return object_instance

    async def delete(self, id: str) -> Transaction:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Transaction).where(Transaction.id == id)
                result = await session.execute(stmt)
                object_instance = result.scalars().first()

                if not object_instance:
                    raise ValueError(f'Transaction with ID {id} not found.')

                await session.delete(object_instance)
                await session.commit()
                return object_instance

    async def add_category(self, id: str, id_category: str) -> Transaction:
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
                    raise RecordNotFoundError('Transaction', id)

                category = await session.get(Category, id_category)

                if not category:
                    raise RecordNotFoundError('Category', id_category)

                transaction.categories.append(category)

                await session.commit()
                return transaction
