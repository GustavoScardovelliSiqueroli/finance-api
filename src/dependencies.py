from fastapi import Depends, Request

from src.domain.rep_interfaces.user_rep_interface import UserRepInterface
from src.services.user_service import UserService


# REPOSITORIES
def get_user_repository(request: Request) -> UserRepInterface:
    return request.app.state.user_repository


# SERVICES
def get_user_service(
    repo: UserRepInterface = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)
