from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession 
import pytest
from typing import AsyncGenerator
import asyncio
from user_service.db.database import Base

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
@pytest.fixture(scope="session")
async def postgres_url():
    with PostgresContainer("postgres:13") as postgres:
        psql_url= postgres.get_connection_url().replace("psycopg2", "asyncpg")
        yield psql_url

@pytest.fixture(scope="session")
async def async_engine(postgres_url:str):
    engine = create_async_engine(postgres_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose() 
@pytest.fixture(scope="function")
async def db_session(async_engine)-> AsyncGenerator[AsyncSession, None]:
    AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False) 
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
