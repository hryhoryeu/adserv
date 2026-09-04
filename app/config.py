from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    user: str = "adserv"
    password: SecretStr = SecretStr("password123")
    host: str = "localhost"
    port: int = 5432
    db: str = "adserv"
    # echo: bool = bool


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
