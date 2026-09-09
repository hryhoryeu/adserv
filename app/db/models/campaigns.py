import datetime
import uuid

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.enums import CampaignStatus


class Campaign(Base):
    __tablename__ = "campaign"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    advertiser_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("advertiser.id"))
    name: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(Enum(CampaignStatus, native_enum=False))
    daily_budget: Mapped[int] = mapped_column(Numeric())
    starts_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    ends_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
