import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt

from src.config import Config
from src.domain.exceptions.auth_exceptions import (
    AuthenticationError,
)
from src.domain.models.user import User
from src.domain.rep_interfaces.user_rep_interface import (
    UserRepInterface,
)

config = Config()


class UserService:
    def __init__(self, repository: UserRepInterface) -> None:
        self.repository = repository

    async def login_user(self, login: str, password: str) -> str:
        user = await self.repository.get_by_login(login)
        if not user:
            raise AuthenticationError('Invalid login or password')
        if not self.__verify_password(password, user.password):
            raise AuthenticationError('Invalid login or password')
        token: str = self.__generate_jwt_token(user)
        return token

    async def register_user(
        self,
        data: User,
    ) -> User:
        data.id = str(uuid.uuid4())  # type: ignore
        data.password = self.__hash_password(data.password)
        data.criado = datetime.now()  # type: ignore
        return await self.repository.create(data)

    async def get_all_user(self) -> list[Optional[User]]:
        return await self.repository.get_all()

    def __hash_password(self, password: ...) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def __verify_password(self, plain_password: str, hashed_password: ...) -> bool:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), hashed_password.encode('utf-8')
        )

    def __generate_jwt_token(self, user: User) -> str:
        payload: dict[str, str] = {
            'user_id': str(user.id),
            'login': str(user.login),
            'exp': str(datetime.now(timezone.utc) + timedelta(hours=24)),
        }
        token: str = jwt.encode(payload, config.API_KEY, 'HS256')
        return token
