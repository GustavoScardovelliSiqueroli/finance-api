from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.api.schemas.transaction_schemas import TransactionCreate, TransactionResponse
from src.cross_cutting.dependencies import get_transaction_service
from src.domain.models.transaction import Transaction
from src.services.transaction_service import TransactionService

router = APIRouter(prefix='/transactions', tags=['transactions'])

"""
    TODO: Add authentication and authorization
    Verify if the user is the owner of the transaction
    with middleware or dependency
"""


@router.get(
    '',
    response_model=list[TransactionResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_transactions(
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> list[TransactionResponse]:
    transactions = await transaction_service.get_all_transaction()
    transactions_reponse: list[TransactionResponse] = [
        TransactionResponse.model_validate(transaction) for transaction in transactions
    ]
    return transactions_reponse


@router.get(
    '/{id}',
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
async def get_transaction_by_id(
    id: str,
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    try:
        transaction = await transaction_service.get_transaction_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Transaction not found'
        )
    return TransactionResponse.model_validate(transaction)


@router.post(
    '',
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    request: Request,
    data: TransactionCreate,
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    transaction_model = Transaction(**TransactionCreate.model_dump(data))
    user_id = UUID(request.state.user['user_id'])
    transaction_model.id_user = user_id
    transaction = await transaction_service.create_transaction(transaction_model)
    return TransactionResponse.model_validate(transaction)


@router.put(
    '/{id}',
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
async def update_transaction(
    id: str,
    data: TransactionCreate,
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    try:
        transaction = await transaction_service.update_transaction(
            id, TransactionCreate.model_dump(data)
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return TransactionResponse.model_validate(transaction)


@router.delete(
    '/{id}',
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_transaction(
    id: str,
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    try:
        transaction = await transaction_service.delete_transaction(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return TransactionResponse.model_validate(transaction)
