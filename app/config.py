from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    user: str
    password: SecretStr
    host: str = "localhost"
    port: int = 5432
    db: str
    # echo: bool = bool


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__", extra="ignore"
    )

    env: Literal["prod", "docker", "local"]
    debug: bool = False
    db: DatabaseSettings


@lru_cache
def get_db_settings():
    return Settings()
