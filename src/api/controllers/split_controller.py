from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.api.schemas.split_schemas import SplitCreateList, SplitResponse
from src.cross_cutting.dependencies import get_transaction_service
from src.services.transaction_service import TransactionService

router = APIRouter(prefix='/transactions/{id_transaction}/splits', tags=['splits'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_splits(
    request: Request,
    id_transaction: int,
    data: SplitCreateList,
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> list[SplitResponse]:
    id_user = UUID(request.state.user['user_id'])
    try:
        splits = await transaction_service.add_splits(
            id_transaction, [split.model_dump() for split in data.splits], id_user
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    return [SplitResponse.model_validate(split) for split in splits]


@router.delete('', status_code=status.HTTP_200_OK)
async def remove_splits(
    request: Request,
    id_transaction: int,
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> list[SplitResponse]:
    id_user = UUID(request.state.user['user_id'])
    try:
        splits = await transaction_service.remove_splits(id_transaction, id_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    return [SplitResponse.model_validate(split) for split in splits]
