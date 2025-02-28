from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.domain.models.enums.type_enum import Type


class CategoryDTO(BaseModel):
    id: int
    id_user: UUID
    name: str
    type: Type
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class CreateCategoryDTO(BaseModel):
    name: str
    type: Type

    class Config:
        orm_mode = True
