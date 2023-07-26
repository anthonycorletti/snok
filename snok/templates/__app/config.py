import os
import sys

from {{ __template_name }}.const import ENV
from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    #
    #   Required
    #
    ENV: str = Field(
        ...,
        env="ENV",
        description=f"Environment, can be one of {list(map(lambda x: x.value, ENV))}",
    )
    API_SECRET_KEY: str = Field(
        ...,
        env="API_SECRET_KEY",
        description="The API secret key.",
    )
    APP_URL: str = Field(
        ...,
        env="APP_URL",
        description="The root url.",
    )
    #
    #   Defaults
    #
    LOG_LEVEL: str = Field(
        "WARNING",
        env="LOG_LEVEL",
        description="Logging level, can be one of DEBUG, "
        "INFO, WARNING, ERROR, CRITICAL",
    )
    #
    #   Postgres
    #
    POSTGRES_SCHEME: str = Field(
        "postgresql+asyncpg",
        env="POSTGRES_SCHEME",
        description="The postgres scheme.",
    )
    POSTGRES_USER: str = Field(
        "{{ __template_name }}",
        env="POSTGRES_USER",
        description="The postgres user.",
    )
    POSTGRES_PASSWORD: str = Field(
        "{{ __template_name }}",
        env="POSTGRES_PASSWORD",
        description="The postgres password.",
    )
    POSTGRES_HOST: str = Field(
        "127.0.0.1",
        env="POSTGRES_HOST",
        description="The postgres host.",
    )
    POSTGRES_PORT: int = Field(
        5432,
        env="POSTGRES_PORT",
        description="The postgres port.",
    )
    POSTGRES_DATABASE: str = Field(
        "{{ __template_name }}_development",
        env="POSTGRES_DATABASE",
        description="The postgres database name.",
    )
    DB_POOL_SIZE: int = Field(
        0,
        env="DB_POOL_SIZE",
        description="The database pool size. 0 indicates no limit.",
    )
    DB_MAX_OVERFLOW: int = Field(
        -1,
        env="DB_MAX_OVERFLOW",
        description="The database max overflow. -1 indicates no limit.",
    )
    DB_POOL_PRE_PING: bool = Field(
        True,
        env="DB_POOL_PRE_PING",
        description="Check database connection before using it.",
    )

    @property
    def db_url(self) -> str:
        return PostgresDsn.build(
            scheme=self.POSTGRES_SCHEME,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=str(self.POSTGRES_PORT),
            path=f"/{self.POSTGRES_DATABASE}",
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



def _set_settings() -> Settings:
    _env = ENV(os.environ["ENV"].lower()) if os.getenv("ENV") else ENV.dev
    # override for test
    if os.getenv("_", "").endswith("pytest") or "pytest" in "".join(sys.argv):
        _env = ENV.test
    Settings.Config.env_file = f".env.{_env.value}"
    return Settings()  # type: ignore


settings = _set_settings()
