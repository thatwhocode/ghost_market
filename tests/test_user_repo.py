import uuid
import pytest
from user_service.repositories.user_repo import UserRepository
from user_service.schemas.user import UserCreate
from shared_packages.db.user import User
from sqlalchemy import select
@pytest.mark.asyncio 
async def test_user_repository_creates_user(db_session):
    repo = UserRepository(session=db_session)
    unique_suffix = str(uuid.uuid4())[:8] # Надійніше за random
    
    user_data = UserCreate(
        username=f"user_{unique_suffix}",
        email=f"test_{unique_suffix}@test.com",
        password="password123"
    )
    
    created_user = await repo.create_user(user_data=user_data)
    
    # Важливо: якщо create_user робить commit, сесія може закритися 
    # або об'єкт стане expired. Використовуйте db_session.refresh(created_user) за потреби.
    
    assert created_user.id is not None
    
    # Перевірка через прямий запит в БД
    stmt = select(User).where(User.email == user_data.email)
    result = await db_session.execute(stmt)
    user_in_db = result.scalar_one_or_none()
    
    assert user_in_db is not None
    assert user_in_db.email == user_data.email