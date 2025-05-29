from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from src.api.schemas.balance_schemas import BalanceResponse
from src.cross_cutting.dependencies import get_transaction_service
from src.services.transaction_service import TransactionService

router = APIRouter(prefix='/balance', tags=['balance'])

"""
    TODO: Add authentication and authorization
    Verify if the user is the owner of the balance
    with middleware or dependency
"""


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=BalanceResponse,
)
async def get_balance(
    request: Request,
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> BalanceResponse:
    id_user = UUID(request.state.user['user_id'])
    balance = await transaction_service.get_balance(id_user)
    return BalanceResponse(balance=balance)
