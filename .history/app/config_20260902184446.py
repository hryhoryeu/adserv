from pydantic import computed_field, SecretStr, PostgresDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    @computed_field
    @property
    def database_url(self) -> str:
        pass


config = Config()
