from fastapi import Depends, Request

from src.domain.rep_interfaces.category_rep_interface import CategoryRepInterface
from src.domain.rep_interfaces.split_rep_interface import SplitRepInterface
from src.domain.rep_interfaces.transaction_rep_interface import TransactionRepInterface
from src.domain.rep_interfaces.user_rep_interface import UserRepInterface
from src.services.category_service import CategoryService
from src.services.split_service import SplitService
from src.services.transaction_service import TransactionService
from src.services.user_service import UserService


# REPOSITORIES
def get_user_repository(request: Request) -> UserRepInterface:
    return request.app.state.user_repository


def get_category_repository(request: Request) -> CategoryRepInterface:
    return request.app.state.category_repository


def get_transaction_repository(request: Request) -> TransactionRepInterface:
    return request.app.state.transaction_repository


def get_split_repository(request: Request) -> SplitRepInterface:
    return request.app.state.split_repository


# SERVICES
def get_user_service(
    repo: UserRepInterface = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)


def get_category_service(
    repo: CategoryRepInterface = Depends(get_category_repository),
) -> CategoryService:
    return CategoryService(repo)


def get_split_service(
    repo: SplitRepInterface = Depends(get_split_repository),
) -> SplitService:
    return SplitService(repo)


def get_transaction_service(
    repo: TransactionRepInterface = Depends(get_transaction_repository),
    category_service: CategoryService = Depends(get_category_service),
    split_service: SplitService = Depends(get_split_service),
) -> TransactionService:
    return TransactionService(repo, category_service, split_service)
