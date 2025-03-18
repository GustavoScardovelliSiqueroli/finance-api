from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.domain.models.enums.type_enum import Type


class BaseTransaction(BaseModel):
    class Config:
        from_attributes = True


class TransactionResponse(BaseTransaction):
    id: int
    id_user: UUID
    value: float
    description: Optional[str]
    type: Type
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class TransactionCreate(BaseTransaction):
    value: float
    description: Optional[str]
    type: Type


class TransactionUpdate(BaseTransaction):
    value: Optional[float]
    description: Optional[str]
    type: Optional[Type]
