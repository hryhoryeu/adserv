import datetime
import uuid

from sqlalchemy import TIMESTAMP, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Adevertiser(Base):
    __tablename__ = "advertiser"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
