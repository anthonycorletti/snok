import os
import sys
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from {{ __template_name }}.config import settings


def _override_db_url_for_distributed_testing() -> None:
    if os.getenv("_", "").endswith("pytest") or "pytest" in "".join(sys.argv):
        pid = os.getpid()
        settings.POSTGRES_DATABASE = f"{settings.POSTGRES_DATABASE}_{pid}"


_override_db_url_for_distributed_testing()


async_db_engine = create_async_engine(
    url=settings.db_url,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    future=True,
)


async def db_session() -> AsyncGenerator:
    async_session = sessionmaker(
        async_db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
