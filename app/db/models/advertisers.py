import datetime
import uuid

from sqlalchemy import TIMESTAMP, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Advertiser(Base):
    __tablename__ = "advertiser"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
