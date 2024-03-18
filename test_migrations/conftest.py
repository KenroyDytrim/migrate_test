import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from db_utils import alembic_config_from_url, tmp_database

import os
from yarl import URL
from config import settings

@pytest.fixture()
def pg_url():
    return URL(os.getenv('CI_STAFF_PG_URL', settings.POSTGRES_DATABASE_URLA))

@pytest.fixture()
async def postgres(pg_url):
    async with tmp_database(pg_url, "pytest") as tmp_url:
        yield tmp_url


@pytest.fixture()
async def postgres_engine(postgres):
    engine = create_async_engine(
        url=postgres,
        pool_pre_ping=True,
    )
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture()
def alembic_config(postgres):
    return alembic_config_from_url(postgres)