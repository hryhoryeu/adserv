from pydantic import PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    @computed_field
    @property
    def database_url(self) -> str:
        return PostgresDsn()


config = Config()
