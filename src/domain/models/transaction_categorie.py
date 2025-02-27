from sqlalchemy import Column, ForeignKey, Integer, Table

from src.domain.models.base import Base

transactions_categories = Table(
    'transactions_categories',
    Base.metadata,
    Column('transaction_id', Integer, ForeignKey('transactions.id')),
    Column('category_id', Integer, ForeignKey('categories.id')),
)
