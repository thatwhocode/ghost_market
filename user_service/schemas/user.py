from pydantic import BaseModel,   EmailStr, Field, SecretStr
from uuid import UUID
from shared_packages.schemas.base import CoreModel
from datetime import datetime
class UserBase(CoreModel):
    email:  EmailStr
    username: str = Field(..., min_length=3, max_length=50, examples=['cool_user_123'])

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be 8 charactes long")

class UserRead(UserBase):
    id: UUID
    is_active: bool =True
    is_superuser: bool
    created_at : datetime
    wallet_echoes : int = 0
    shards : int = 0
    reputation: int = 0
class UserLoginEmail(CoreModel):
    email: EmailStr
    password: SecretStr
class UserLoginUsername(CoreModel):
    username: str
    password: SecretStr
class UserLogin(UserLoginUsername):
    email: EmailStr
class UserUpdate(CoreModel):
    username : str
class UserShort(CoreModel):
    username: str 
class UserAdminView(UserRead):
    is_active : bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
class AdminStatsRead(CoreModel):
    total_users: int = Field(..., description="Quantity of registered players")
    total_economy: int = Field(..., description="Wallet echo curency")
    admins_count: int = Field(..., description="Quantity of admins")