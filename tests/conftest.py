import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from testcontainers.postgres import PostgresContainer
from user_service.db.database import Base, get_db  # get_db — це твій dependency у FastAPI
from httpx import AsyncClient, ASGITransport
from user_service.main import app
from shared_packages.core.security import create_access_token # Твоя функція створення токенів
from uuid import uuid4
@pytest.fixture
def regular_user_token_headers():
    """Повертає заголовок з токеном звичайного користувача."""
    user_id = str(uuid4())
    access_token = create_access_token(data={"sub": user_id, "email": "user@test.com", "is_admin": False})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def admin_token_headers():
    """Повертає заголовок з токеном адміністратора."""
    user_id = str(uuid4())
    access_token = create_access_token(data={"sub": user_id, "email": "user@test.com", "is_admin": True})
    return {"Authorization": f"Bearer {access_token}"}
@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """Створює асинхронний клієнт та підміняє залежність get_db."""
    
    # Внутрішня функція для override
    async def _override_get_db():
        yield db_session

    # Підміняємо реальний get_db на тестову сесію
    app.dependency_overrides[get_db] = _override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app, raise_app_exceptions= True), base_url="http://test") as ac:
        yield ac
    
    # Обов'язково чистимо підміну після тесту
    app.dependency_overrides.clear()
@pytest_asyncio.fixture(scope="function")
async def async_engine():
    """Створює двигун БД один раз на всю сесію тестів."""
    with PostgresContainer("postgres:15-alpine") as postgres:
        psql_url = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        engine = create_async_engine(psql_url)
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        yield engine
        await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(async_engine):
    """Створює чисту сесію для кожного тесту і відкочує зміни після завершення."""
    connection = await async_engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection, expire_on_commit=False)
 
    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()