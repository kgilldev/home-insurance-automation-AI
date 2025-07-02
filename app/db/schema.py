from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy import JSON, TIMESTAMP, Enum
from datetime import datetime, timezone

from app.enum.enums import DecisionStatus


Base = declarative_base()

class Claims(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name:Mapped[str] = mapped_column(nullable=False)
    parsed_text:Mapped[str] = mapped_column(nullable=False)
    structured_claim:Mapped[dict] = mapped_column(JSON, nullable=False)
    decision:Mapped[DecisionStatus] = mapped_column(Enum(DecisionStatus), nullable=False)
    created_at:Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
