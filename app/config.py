from functools import lru_cache
from typing import Literal

import sqlalchemy as sa
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    user: str = "adserv"
    password: SecretStr = SecretStr("password123")
    host: str = "localhost"
    port: int = 5432
    name: str = "adserv"
    pool_size: int = 5
    max_overflow: int = 10
    echo_pool: bool = False
    echo: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__", extra="ignore"
    )

    env: Literal["prod", "docker", "local"] = "local"
    debug: bool = False
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)


@lru_cache
def get_settings():
    return Settings()


def get_database_url():
    settings = get_settings()
    return sa.URL.create(
        "postgresql+asyncpg",
        username=settings.db.user,
        password=settings.db.password.get_secret_value(),
        host=settings.db.host,
        port=settings.db.port,
        database=settings.db.name,
    )
