import re
from typing import Optional, Sequence

import aiomysql  # type: ignore
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.db_exceptions import DuplicateRecordError, ForeignKeyError
from src.domain.models.split import Split
from src.domain.rep_interfaces.split_rep_interface import SplitRepInterface
from src.infra.db.database import async_session


class SplitRepository(SplitRepInterface):
    def __init__(
        self, session: async_sessionmaker[AsyncSession] = async_session
    ) -> None:
        self.session = session

    async def get_all(self) -> Sequence[Split]:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Split)
                result = await session.execute(stmt)
                return result.scalars().all()

    async def create(self, data: Split) -> Split:
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

    async def get_by_id(self, id: str) -> Optional[Split]:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Split).where(Split.id == id)
                result = await session.execute(stmt)
                return result.scalars().first()

    async def update(self, id: str, data: Split) -> Split:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Split).where(Split.id == id)
                result = await session.execute(stmt)
                object_instance = result.scalars().first()

                if not object_instance:
                    raise ValueError(f'Split com ID {id} não encontrada')

                for key, value in data.as_dict().items():
                    if key != 'id' and hasattr(object_instance, key):
                        setattr(object_instance, key, value)

                session.add(object_instance)
                await session.commit()

                return object_instance

    async def delete(self, id: str) -> Split:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Split).where(Split.id == id)
                result = await session.execute(stmt)
                object_instance = result.scalars().first()

                if not object_instance:
                    raise ValueError(f'Split com ID {id} não encontrada')

                await session.delete(object_instance)
                await session.commit()
                return object_instance

    async def create_many(self, data: list[Split]) -> list[Split]:
        async with self.session() as session:
            successful_items: list[Split] = []
            failed_items: list[tuple[Split, str]] = []

            for item in data:
                async with session.begin():
                    try:
                        session.add(item)
                        await session.flush()
                        successful_items.append(item)
                    except IntegrityError as e:
                        await session.rollback()
                        failed_items.append((item, str(e)))
                        continue

            return successful_items

    async def delete_all(self, id_transaction: int) -> Sequence[Split]:
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(
                    delete(Split)
                    .where(Split.id_transaction == id_transaction)
                    .returning(Split)
                )
                deleted_splits = result.scalars().all()
                return deleted_splits

    async def get_all_by_id_transaction(self, id_transaction: int) -> Sequence[Split]:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Split).where(Split.id_transaction == id_transaction)
                result = await session.execute(stmt)
                return result.scalars().all()
