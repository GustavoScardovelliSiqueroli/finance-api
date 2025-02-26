from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry

from src.config import Config

config = Config()  # type: ignore

async_connection_string = f'mysql+aiomysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'

async_engine = create_async_engine(async_connection_string, echo=True)

async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
table_registry = registry()
