from functools import lru_cache

from pydantic import PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="POSTGRES_")

    user: str
    password: SecretStr
    host: str = "localhost"
    port: int = 5432
    db: str

    @computed_field
    @property
    def database_url(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
        )


@lru_cache
def get_db_settings():
    return PostgresSettings()
