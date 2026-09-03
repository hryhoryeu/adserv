from pydantic_settings import BaseSettings


class Config(BaseSettings):
    var1: str


config = Config()
