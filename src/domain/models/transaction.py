from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import UUID as UUIDdb
from sqlalchemy import DateTime, Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.base import Base
from src.domain.models.enums.type_enum import Type


class Transaction(Base):
    __tablename__ = 'transactions'
    id: Mapped[UUID] = mapped_column(UUIDdb, primary_key=True, default=uuid4)
    id_user: Mapped[UUID] = mapped_column(UUIDdb, nullable=False, foreignKey='users.id')
    value: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=False)
    type: Mapped[Type] = mapped_column(Enum(Type), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password
