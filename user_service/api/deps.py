from user_service.services.auth_service import AuthService
from user_service.repositories.user_repo import UserRepository
from fastapi.security import OAuth2PasswordBearer
from user_service.db.database import get_db
from user_service.services.redis import RedisService
from fastapi import Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from shared_packages.db.user import User
from fastapi import HTTPException, status
from shared_packages.core.config import SharedBaseSettings, RedisSettings
from shared_packages.core.security import decode_access_token
from user_service.schemas.user import UserRead
stgs = SharedBaseSettings()
redis_stgs = RedisSettings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{stgs.APP_VERSION}/auth/token")

def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_redis_service(request : Request)-> RedisService:
    return request.app.state.redis
async def get_validated_payload(token: str =Depends(oauth2_scheme), redis : RedisService = Depends(get_redis_service))-> dict:
        payload = decode_access_token(token)
        print(f"DEBUG: payload type is {type(payload)}, value is {payload}")
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        jti = payload.get("jti")
        if not jti:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Jti is missing")
        if await redis.is_in_blacklist(jti):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        blacklisted = await redis.is_in_blacklist(jti)
        print(f"DEBUG BLACKLIST: jti={jti}, is_blacklisted={blacklisted}")
    
        if blacklisted:
            print("DEBUG: Blocking request because token is in blacklist")
            raise HTTPException(status_code=401, detail="Token expired/Logged out")
        
        return payload
    
async def get_current_user( payload: dict = Depends(get_validated_payload), user_repo: UserRepository = Depends(get_user_repo)) -> UserRead:
        user_id = payload.get("sub")
        print(f"DEBUG IN CURRENT_USER: type is {type(payload)}, value is {payload}")
        user = await user_repo.find_user_by_id(user_id)
        if not user: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
        return user
class Dependencies:
    def __init__(self, db : AsyncSession =Depends(get_db)):
        self.db = db
    @property
    def user_repo(self) -> UserRepository:
        return UserRepository(self.db)
    @property
    def auth_service(self) -> AuthService:
        return AuthService(self.user_repo)
class AdminRequired:
    async def __call__(self, deps: Dependencies = Depends(), token:str = Depends(oauth2_scheme)):
        user = await deps.auth_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such user")
        if not user.is_superuser:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="admin role required")
        return user
