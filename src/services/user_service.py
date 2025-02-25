from datetime import datetime, timedelta, timezone
from typing import Final, Optional

import bcrypt
import jwt

from src.config import Config
from src.domain.exceptions.auth_exceptions import (
    AuthenticationError,
    InvalidTokenError,
    TokenExpiredError,
)
from src.domain.models.user import User
from src.domain.rep_interfaces.user_rep_interface import (
    UserRepInterface,
)


class UserService:
    TOKEN_HOURS: Final[int] = 1
    REFRESH_TOKEN_DAYS: Final[int] = 7

    def __init__(self, repository: UserRepInterface) -> None:
        self.repository = repository

    async def login_user(self, login: str, password: str) -> tuple[str, str]:
        user = await self.repository.get_by_login(login)
        if not user:
            raise AuthenticationError('Invalid login or password')
        if not self.__verify_password(password, user.password):
            raise AuthenticationError('Invalid login or password')
        token, refresh_token = self.__generate_jwt_token(user)
        return token, refresh_token

    async def register_user(self, login: str, password: str) -> User:
        hashed_password: str = self.__hash_password(password)
        user = User(login=login, password=hashed_password)
        return await self.repository.create(user)

    async def refresh_token(self, refresh_token: str) -> tuple[str, str]:
        try:
            payload: dict[str, str] = jwt.decode(
                refresh_token, Config.API_KEY, algorithms=[Config.ALGORITHM]
            )
            user_id: str = payload['user_id']
            user: Optional[User] = await self.repository.get_by_id(user_id)
            if not user:
                raise InvalidTokenError('Invalid refresh token')
            token, refresh_token = self.__generate_jwt_token(user)
            return token, refresh_token
        except jwt.ExpiredSignatureError as e:
            raise TokenExpiredError('Refresh token has expired') from e
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError('Invalid refresh token') from e

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

    def __generate_jwt_token(self, user: User) -> tuple[str, str]:
        payload: dict[str, str] = {
            'user_id': str(user.id),
            'login': str(user.login),
            'exp': str(datetime.now(timezone.utc) + timedelta(hours=self.TOKEN_HOURS)),
        }
        token: str = jwt.encode(payload, Config.API_KEY, 'HS256')
        refresh_payload: dict[str, str] = {
            'user_id': str(user.id),
            'login': str(user.login),
            'exp': str(
                datetime.now(timezone.utc) + timedelta(days=self.REFRESH_TOKEN_DAYS)
            ),
        }
        refresh_token: str = jwt.encode(refresh_payload, Config.API_KEY, 'HS256')
        return token, refresh_token
