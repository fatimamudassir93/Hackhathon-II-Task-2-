from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import AsyncAdaptedQueuePool, QueuePool
from ..config import settings
import os
import ssl as ssl_module
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def _prepare_asyncpg_url(url: str):
    """Strip sslmode from URL and return (clean_url, connect_args).
    asyncpg doesn't accept sslmode as a query param; it needs ssl=True in connect_args."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    use_ssl = "sslmode" in params and params["sslmode"][0] != "disable"
    params.pop("sslmode", None)
    clean_query = urlencode({k: v[0] for k, v in params.items()})
    clean_url = urlunparse(parsed._replace(query=clean_query))
    connect_args = {"ssl": "require"} if use_ssl else {}
    return clean_url, connect_args

_async_url, _async_connect_args = _prepare_asyncpg_url(settings.DATABASE_URL)

# Async database engine
async_engine = create_async_engine(
    _async_url,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False,  # Set to True for debugging
    connect_args=_async_connect_args,
)

async def get_async_session():
    async with AsyncSession(async_engine) as session:
        yield session

# For sync operations if needed (psycopg2 handles sslmode in URL natively)
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