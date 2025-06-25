from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import TIMESTAMP, Column, Integer, String, JSON

Base = declarative_base()

class Claims(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    parsed_text = Column(String, nullable=False)
    structured_claim = Column(JSON, nullable=False)
    decision = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)



