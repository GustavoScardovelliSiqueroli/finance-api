import re
from typing import Optional

import aiomysql  # type: ignore
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.domain.exceptions.db_exceptions import DuplicateRecordError, ForeignKeyError
from src.domain.models.user import User
from src.domain.rep_interfaces.user_rep_interface import UserRepInterface
from src.infra.db.database import async_session


class UserRepository(UserRepInterface):
    async def get_all(self) -> list[Optional[User]]:
        async with async_session() as session:
            async with session.begin():
                stmt = select(User)
                result = await session.execute(stmt)
                return result.scalars().all()  # type:ignore

    async def create(self, data: User) -> User:
        try:
            async with async_session() as session:
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

    async def get_by_login(self, login: str) -> Optional[User]:
        async with async_session() as session:
            async with session.begin():
                stmt = select(User).where(User.login == login)
                result = await session.execute(stmt)
                return result.scalars().first()

    async def get_by_id(self, id: str) -> Optional[User]: ...

    async def update(self, id: str, data: User) -> User: ...

    async def delete(self, id: str) -> User: ...
