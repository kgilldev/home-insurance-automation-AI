from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DB = os.getenv("DB_URL")

if not DB:
    raise ValueError("DB is not found. Check DB URL")

engine = create_engine(DB)
SessionLocal = sessionmaker(bind=engine)