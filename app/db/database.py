from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()
SYNC_DB = os.getenv("DB_URL_SYNC")
ASYNC_DB = os.getenv("DB_URL_ASYNC")

if not SYNC_DB:
    raise ValueError("DB is not found. Check SYNC_DB URL")
if not ASYNC_DB:
    raise ValueError("DB is not found. Check ASYNC_DB URL")

sync_engine = create_engine(SYNC_DB)
SessionLocal = sessionmaker(bind=sync_engine)

async_engine = create_async_engine(ASYNC_DB, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)