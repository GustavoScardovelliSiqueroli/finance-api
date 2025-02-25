from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class SuccessResponse(BaseModel, Generic[T]):
    # success: bool = True
    # message: Optional[str] = None
    data: Optional[T] = None
    pagination: Optional[dict[str, Any]] = None
    # meta: Optional[dict[str, Any]] = None


# class ErrorResponse(BaseModel):
#     success: bool = False
#     details: Optional[dict[str, Any]] = None
#     meta: Optional[dict[str, Any]] = None
