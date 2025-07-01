from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, JSON, DateTime, TIMESTAMP
import datetime


Base = declarative_base()

class Claims(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    parsed_text = Column(String, nullable=False)
    structured_claim = Column(JSON, nullable=False)
    decision = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

