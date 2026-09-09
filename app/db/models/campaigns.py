import datetime
import uuid
from decimal import Decimal

from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Enum,
    ForeignKey,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.enums import CampaignStatus


class Campaign(Base):
    __tablename__ = "campaign"
    __table_args__ = (
        CheckConstraint("daily_budget > 0", name="daily_budget_positive"),
        CheckConstraint("ends_at IS NULL OR ends_at > starts_at", name="valid_period"),
        CheckConstraint(
            "status IN ({})".format(", ".join(f"'{s.value}'" for s in CampaignStatus)),
            name="valid_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    advertiser_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("advertiser.id"), index=True
    )
    name: Mapped[str] = mapped_column(String(50))
    status: Mapped[CampaignStatus] = mapped_column(
        Enum(
            CampaignStatus,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=CampaignStatus.DRAFT,
    )
    daily_budget: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    starts_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
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
