from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from .database import async_engine

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session for dependency injection
    """
    async with AsyncSession(async_engine) as session:
        try:
            yield session
        finally:
            await session.close()