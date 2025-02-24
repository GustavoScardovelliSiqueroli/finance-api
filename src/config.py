from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_USER: str = 'dev'
    DB_PASSWORD: str = 'dev123'
    DB_HOST: str = 'dbfinance'
    DB_NAME: str = 'finance'
    MYSQL_ROOT_PASSWORD: str = 'dev123'
    MYSQL_DATABASE: str = 'finance'
    MYSQL_USER: str = 'dev'
    MYSQL_PASSWORD: str = 'dev123'
    DB_PORT: int = 3307
    API_KEY: str = 'apikeydev'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    def get_db_url_alembic(self) -> str:
        return f'mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
