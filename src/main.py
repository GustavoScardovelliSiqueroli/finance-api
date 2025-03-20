from fastapi import FastAPI

from src.api.controllers.auth_controller import router as user_router
from src.api.controllers.transaction_controller import router as transaction_router
from src.cross_cutting.middlewares import AuthMiddleware
from src.infra.db.repositories.category_repository import CategoryRepository
from src.infra.db.repositories.split_repository import SplitRepository
from src.infra.db.repositories.transaction_repository import TransactionRepository
from src.infra.db.repositories.user_repository import UserRepository


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(AuthMiddleware)

    app.state.user_repository = UserRepository()
    app.state.category_repository = CategoryRepository()
    app.state.split_repository = SplitRepository()
    app.state.transaction_repository = TransactionRepository()

    app.include_router(user_router)
    app.include_router(transaction_router)
    return app


app = create_app()
