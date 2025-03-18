from fastapi import APIRouter, status

from src.api.schemas.transaction_schemas import TransactionResponse

router = APIRouter(prefix='/transactions', tags=['transactions'])


@router.get(
    '',
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def get_all_transactions() -> TransactionResponse: ...
