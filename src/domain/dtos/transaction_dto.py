from pydantic import BaseModel


class TransactionDTO(BaseModel):
    id: str
    value: float
    description: str
    type: str
    created_at: str
    updated_at: str
    deleted_at: str

    class Config:
        from_attributes = True


class CreateTransictionDTO(BaseModel):
    value: float
    description: str
    type: str
