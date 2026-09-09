import datetime
import uuid
from decimal import Decimal

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.enums import CampaignStatus


class Campaign(Base):
    __tablename__ = "campaign"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    advertiser_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("advertiser.id"))
    name: Mapped[str] = mapped_column(String(50))
    status: Mapped[CampaignStatus] = mapped_column(
        Enum(
            CampaignStatus,
            native_enum=False,
            create_constraint=True,
            name="ck_campaign_status",
            values_callable=lambda x: [e.value for e in x],
        ),
        default=CampaignStatus.DRAFT,
    )
    daily_budget: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    starts_at: Mapped[datetime.datetime] = (
        mapped_column(TIMESTAMP(timezone=True), server_default=func.now()),
    )
    ends_at: Mapped[datetime.datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
