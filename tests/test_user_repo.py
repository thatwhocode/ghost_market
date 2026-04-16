from user_service.repositories.user_repo import UserRepository
from user_service.schemas.user import UserCreate
import random
from user_service.core.security import get_password_hash
from sqlalchemy import select
from shared_packages.db.user import User
async def test_user_repository_creates_user(db_session):

    repo = UserRepository(session=db_session)
    rand_int = random.randint(1,128) 
    
    user_data  = UserCreate(username=f"test_user_{rand_int}",email=f"test_user_{rand_int}@test.com",password="password123")
    created_user =  await repo.create_user(user_data=user_data)
    
    assert created_user.id is not None
    assert created_user.email == f"test_user_{rand_int}@test.com"
    stmt = select(User).where(User.email == user_data.email)
    result  = await db_session.execute(stmt)
    user = result.scalar_one_or_none()
    assert(user is not None)
    assert(user.email == user_data.email)
    