from pathlib import Path, PosixPath
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from yarl import URL
from enum import Enum

from app.api.utils.connection_manager import ConnectionManager
from .api.authorization.settings import AuthJWT

class LogLevel(str, Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """
    # FastAPI
    DIRECTORY: PosixPath = Path(__file__).resolve().parent.parent

    DOMEN:str = 'localhost'

    PROJECT_TITLE: str
    # FastAPI
    FAST_API_PORT: str
    FAST_API_PREFIX: str

    log_level: LogLevel = LogLevel.INFO

    # POSTGRES
    POSTGRES_HOST: str 
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str 

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USER: str
    REDIS_PASSWORD: str

    NEWS_TOKEN: str

    SMTP_EMAIL: str
    SMTP_PASSWORD: str

    auth_jwt: AuthJWT = AuthJWT()
    
    
    manager: ConnectionManager = ConnectionManager()

    @property
    def get_domen(self):
        return f"http://{self.DOMEN}:{self.FAST_API_PORT}{self.FAST_API_PREFIX}"

    def redis_url(self, db) -> URL:
        """
        Assemble redis URL from settings.

        :return: redis URL.
        """
        return URL.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            user=None,
            password=self.REDIS_PASSWORD,
            path=f"/{db}",
        )

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=f"/{self.POSTGRES_DB}",
        )
    
    model_config = SettingsConfigDict(
        env_file=".env.develop",
        env_file_encoding="utf-8",
    )

settings = Settings()
