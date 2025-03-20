from typing import Optional

from pydantic import BaseModel

from src.domain.models.enums.type_enum import Type


class BaseTransaction(BaseModel):
    class Config:
        from_attributes = True


class TransactionResponse(BaseTransaction):
    id: int
    value: float
    description: Optional[str]
    type: Type


class TransactionCreate(BaseTransaction):
    value: float
    description: Optional[str]
    type: Type


class TransactionUpdate(BaseTransaction):
    value: Optional[float]
    description: Optional[str]
    type: Optional[Type]
