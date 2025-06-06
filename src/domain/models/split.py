from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.base import Base


class Split(Base):
    __tablename__ = 'splits'
    id: Mapped[int] = mapped_column(primary_key=True)
    id_transaction: Mapped[int] = mapped_column(ForeignKey('transactions.id'))
    id_category: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)
    amount: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
