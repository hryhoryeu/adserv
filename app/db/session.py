from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import PostgresSettings, get_db_settings


def get_db_url(url: Annotated[PostgresSettings, Depends(get_db_settings)]):
    return url


engine = create_engine(url=get_db_url())

Session = sessionmaker(engine)
