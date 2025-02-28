import re
from typing import Optional

import aiomysql  # type: ignore
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.exceptions.db_exceptions import DuplicateRecordError, ForeignKeyError
from src.domain.models.category import Category
from src.domain.rep_interfaces.category_rep_interface import CategoryRepInterface
from src.infra.db.database import async_session


class CategoryRepository(CategoryRepInterface):
    def __init__(
        self, session: async_sessionmaker[AsyncSession] = async_session
    ) -> None:
        self.session = session

    async def get_all(self) -> list[Optional[Category]]:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Category)
                result = await session.execute(stmt)
                object_instances: list[Optional[Category]] = []
                for object_instance in result.scalars().all():
                    object_instances.append(object_instance)
                return object_instances

    async def create(self, data: Category) -> Category:
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

    async def get_by_id(self, id: str) -> Optional[Category]:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Category).where(Category.id == id)
                result = await session.execute(stmt)
                return result.scalars().first()

    async def update(self, id: str, data: Category) -> Category:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Category).where(Category.id == id)
                result = await session.execute(stmt)
                object_instance = result.scalars().first()

                if not object_instance:
                    raise ValueError(f'Category com ID {id} não encontrada')

                for key, value in data.as_dict().items():
                    if key != 'id' and hasattr(object_instance, key):
                        setattr(object_instance, key, value)

                session.add(object_instance)
                await session.commit()

                return object_instance

    async def delete(self, id: str) -> Category:
        async with self.session() as session:
            async with session.begin():
                stmt = select(Category).where(Category.id == id)
                result = await session.execute(stmt)
                object_instance = result.scalars().first()

                if not object_instance:
                    raise ValueError(f'Category com ID {id} não encontrada')

                await session.delete(object_instance)
                await session.commit()
                return object_instance
