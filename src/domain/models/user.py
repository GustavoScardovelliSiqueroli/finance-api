from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import UUID as UUIDdb
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.base import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(UUIDdb, primary_key=True, default=uuid4)
    login: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    refresh_token: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password
