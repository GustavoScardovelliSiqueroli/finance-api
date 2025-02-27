from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import UUID as UUIDdb
from sqlalchemy import DateTime, Enum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.base import Base
from src.domain.models.categories import Category
from src.domain.models.enums.type_enum import Type
from src.domain.models.transactions_categories import TransactionCategory


class Transaction(Base):
    __tablename__ = 'transactions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_user: Mapped[UUID] = mapped_column(UUIDdb, nullable=False, foreignKey='users.id')
    value: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=False)
    type: Mapped[Type] = mapped_column(Enum(Type), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    transaction_categories: Mapped[list['TransactionCategory']] = relationship(
        'TransactionCategory', back_populates='transaction'
    )
    categories: Mapped[list['Category']] = relationship(
        'Category', secondary='transaction_categories', back_populates='transactions'
    )
