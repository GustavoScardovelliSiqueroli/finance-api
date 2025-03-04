from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.api.schemas.auth_schema import Login, RefreshToken, Token
from src.cross_cutting.dependencies import get_user_service
from src.domain.exceptions.auth_exceptions import AuthenticationError, InvalidTokenError
from src.domain.exceptions.db_exceptions import DuplicateRecordError, ForeignKeyError
from src.services.user_service import UserService

router = APIRouter(prefix='/auth', tags=['users'])


@router.post(
    '/register',
    response_model=RefreshToken,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: Login,
    user_service: UserService = Depends(get_user_service),
) -> RefreshToken:
    try:
        login = data.login
        password = data.password
        await user_service.register_user(login, password)
        token, refresh_token = await user_service.login_user(login, password)
        return RefreshToken(access_token=token, refresh_token=refresh_token)

    except DuplicateRecordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except ForeignKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.post(
    '/login',
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: Optional[Login],
    request: Request,
    user_service: UserService = Depends(get_user_service),
) -> Token:
    if not data:
        refresh_token = request.headers.get('refresh_token')
        if refresh_token:
            try:
                token = await user_service.refresh_token(refresh_token)
                return Token(access_token=token[0])
            except InvalidTokenError as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
                ) from e
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token or login and password required',
            )
    login = data.login
    password = data.password
    try:
        token = await user_service.login_user(login, password)
        return Token(access_token=token[0])
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e


# MAKE ROTE TO RENOVATE REFRESH_TOKEN

# @router.get(
#     '/pessoas',
#     response_model=SuccessResponse[list[Optional[PessoaDTO]]],
#     status_code=status.HTTP_200_OK,
# )
# async def get_all_pessoas(
#     pessoa_use_case: PessoaService = Depends(get_pessoa_service),
# ) -> SuccessResponse[list[Optional[PessoaDTO]]]:
#     pessoas = await pessoa_use_case.get_all_pessoas()
#     response_data: list[Optional[PessoaDTO]] = [
#         PessoaDTO.model_validate(pessoa) for pessoa in pessoas
#     ]
#     return SuccessResponse[list[Optional[PessoaDTO]]](data=response_data)
