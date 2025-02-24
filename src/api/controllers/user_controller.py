from fastapi import APIRouter

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/')
async def test() -> dict[str, str]:
    return {'message': 'test'}
