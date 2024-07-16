from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from yarl import URL
from enum import Enum
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
    fast_api_port: str = Field(default="8000", env="FAST_API_PORT")
    fast_api_title: str = Field(default="FastAPI", env="FAST_API_TITLE")
    fast_api_prefix: str = Field(default="/api/v1", env="FAST_API_PREFIX")


    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    postgres_host: str = Field(default="localhost", env="POSTGRES_HOST")
    postgres_name: str = Field(..., env="POSTGRES_NAME")
    postgres_port: int = Field(..., env="POSTGRES_PORT")
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., env="POSTGRES_DB")

    auth_jwt: AuthJWT = AuthJWT()
    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.postgres_host,
            port=self.postgres_port,
            user=self.postgres_user,
            password=self.postgres_password,
            path=f"/{self.postgres_db}",
        )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
