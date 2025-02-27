from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.base import Base
from src.domain.models.categories import Category
from src.domain.models.transaction import Transaction


class TransactionCategory(Base):
    __tablename__ = 'transaction_categories'

    transaction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('transactions.id'), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('categories.id'), primary_key=True
    )

    transaction: Mapped['Transaction'] = relationship(
        'Transaction', back_populates='transaction_categories'
    )
    category: Mapped['Category'] = relationship(
        'Category', back_populates='transaction_categories'
    )
