#type: ignore
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.domain.models.base import Base
import pytest

@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Cria as tabelas

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session  # Fornece a sessão para os testes

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)