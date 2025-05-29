import jwt
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.config import Config

CONFIG = Config()  # type: ignore


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: ...) -> Response:
        if request.url.path in [
            '/auth/login',
            '/docs',
            '/openapi.json',
            '/auth/register',
        ]:
            return await call_next(request)

        authorization: str | None = request.headers.get('Authorization')
        if not authorization or not authorization.startswith('Bearer '):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'detail': 'Token não fornecido ou inválido'},
            )

        token = authorization.split('Bearer ')[1]

        try:
            payload = jwt.decode(token, CONFIG.API_KEY, algorithms=['HS256'])
            request.state.user = payload
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={'detail': 'Token inválido'},
            )

        response = await call_next(request)
        return response
