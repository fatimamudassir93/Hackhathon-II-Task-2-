from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import AsyncAdaptedQueuePool, QueuePool
from ..config import settings
import os

# Async database engine
async_engine = create_async_engine(
    settings.DATABASE_URL,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False  # Set to True for debugging
)

async def get_async_session():
    async with AsyncSession(async_engine) as session:
        yield session

# For sync operations if needed
sync_engine = create_engine(
    settings.DATABASE_URL.replace("+asyncpg", ""),
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False  # Set to True for debugging
)

def get_session():
    with Session(sync_engine) as session:
        yield session