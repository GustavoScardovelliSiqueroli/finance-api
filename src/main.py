from fastapi import FastAPI

from src.api.controllers.auth_controller import router as user_router
from src.infra.db.repositories.user_repository import UserRepository
from src.middlewares import AuthMiddleware


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(AuthMiddleware)

    app.state.user_repository = UserRepository()

    app.include_router(user_router)
    return app


app = create_app()
