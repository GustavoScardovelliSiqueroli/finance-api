from pydantic import BaseModel


class BaseSplit(BaseModel):
    id_transaction: int
    id_category: int | None
    amount: float

    class Config:
        from_attributes = True


class SplitResponse(BaseSplit):
    id: int


class SplitCreate(BaseModel):
    id_category: int | None
    amount: float


class SplitCreateList(BaseModel):
    splits: list[SplitCreate]
