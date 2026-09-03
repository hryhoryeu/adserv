from pydantic import computed_field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    def database_url():
        pass


config = Config()
