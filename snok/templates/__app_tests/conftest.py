import asyncio
from typing import AsyncGenerator, Generator
from urllib.parse import urlparse

import asyncpg
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import Request
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from {{ __template_name }}.kit.db import RecordModel
from {{ __template_name }}.database import async_db_engine
from {{ __template_name }}.logger import log
from {{ __template_name }}.app import app
from {{ __template_name }}.config import settings

TEST_BASE_URL = "http://testserver:8001"


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator:
    async with AsyncClient(
        app=app,
        base_url=TEST_BASE_URL,
    ) as client, LifespanManager(app):
        yield client


@pytest.fixture(scope="session", autouse=True)
def event_loop(request: Request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_db_session() -> AsyncGenerator:
    session = sessionmaker(
        async_db_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as s:
        async with async_db_engine.begin() as conn:
            await conn.run_sync(RecordModel.metadata.create_all)
        yield s

    async with async_db_engine.begin() as conn:
        await conn.run_sync(RecordModel.metadata.drop_all)

    await async_db_engine.dispose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database() -> AsyncGenerator:
    parsed_url = urlparse(settings.db_url)
    database = parsed_url.path[1:]
    host = parsed_url.hostname
    port = parsed_url.port
    user = parsed_url.username
    password = parsed_url.password

    try:
        conn = await asyncpg.connect(user=user, password=password, host=host, port=port)
        await conn.execute(f"CREATE DATABASE {database};")
    except asyncpg.exceptions.DuplicateDatabaseError:  # pragma: no cover
        log.debug("Database already exists, skipping creation.")
    finally:
        await conn.close()

    yield

    try:
        conn = await asyncpg.connect(user=user, password=password, host=host, port=port)
        await conn.execute(f"DROP DATABASE {database};")
    except asyncpg.exceptions.DuplicateDatabaseError:  # pragma: no cover
        log.debug("Database already exists, skipping creation.")
    finally:
        await conn.close()
