from pydantic import PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="POSTGRES_")
    host: str = None

    @computed_field
    @property
    def database_url(self) -> str:
        return PostgresDsn()


config = Config()
