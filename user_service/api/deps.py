from user_service.services.auth_service import AuthService
from user_service.repositories.user_repo import UserRepository
from fastapi.security import OAuth2PasswordBearer
from user_service.db.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared_packages.db.user import User
from fastapi import HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")
class Dependencies:
    def __init__(self, db : AsyncSession =Depends(get_db)):
        self.db = db
        
    @property
    def user_repo(self) -> UserRepository:
        return UserRepository(self.db)
    @property
    def auth_service(self) -> AuthService:
        return AuthService(self.user_repo)
    
    async def get_current_user(self, token: str) -> User:
        user = await self.auth_service.get_user_from_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    async def get_current_admin(self, token: str = Depends(oauth2_scheme)) -> User:
        user = await self.auth_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        if not user.is_superuser:
            raise HTTPException(status_code=403, detail="Rights required")
        return user