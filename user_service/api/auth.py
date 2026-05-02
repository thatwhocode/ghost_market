from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from user_service.schemas.user import UserCreate, UserLoginEmail, UserRead, UserLoginUsername, UserUpdate, UserShort
from user_service.api.deps import Dependencies, AuthService, oauth2_scheme, AdminRequired
from shared_packages.schemas.token import Token
from uuid import UUID
from user_service.schemas.user import UserBase
import structlog
router = APIRouter()
oauth_schema = OAuth2PasswordBearer(tokenUrl="0.0.0.1/auth/token")
logger = structlog.get_logger()
@router.post("/register",  response_model = UserRead)
async def register(user_data : UserCreate, deps : Dependencies =  Depends(Dependencies)):
    logger.info("register_endpoint_starts")
    result = await deps.auth_service.register_user(user_data=user_data)
    logger.info("user_registered", extra = {"username": f"{user_data.username}"})
    return result
@router.post("/login_via_email", response_model=Token)
async def login_with_email(user_data : UserLoginEmail, deps: Dependencies = Depends(Dependencies)):
    logger.info("user_login_via_email_started")
    logger.info("user_email", extra={"email":f"{user_data.email}"})
    result = await deps.auth_service.login_with_email(user_data=user_data)
    logger.info("user_login_succesfull")
    return result
@router.post("/login_via_username", response_model= Token)
async def login_with_usernmae(user_data: UserLoginUsername, deps: Dependencies = Depends(Dependencies)):
    logger.info("user_login_via_username_started")
    logger.info("user_email", extra={"email":f"{user_data.username}"})
    result = await deps.auth_service.login_with_username(user_data=user_data)
    logger.info("user_login_succesfull")
    return result
@router.post("/token")
async def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    deps: Dependencies = Depends()
):

    if "@" in form_data.username:
        login_data = UserLoginEmail(
            email=form_data.username, 
            password=form_data.password
        )    
        logger.info("user_login_via_email_started_in_oauth_form")
        logger.info("email", extra  = f"{form_data.username}")
        return await deps.auth_service.login_with_email(login_data)
        
    else:
        login_data = UserLoginUsername(
            username=form_data.username, 
            password=form_data.password
        )
        logger.info("user_login_via_username_started_in_oauth_form")
        logger.info("username", extra  = f"{form_data.username}")
        return await deps.auth_service.login_with_username(login_data)
@router.get("/me", response_model=UserRead)
async def get_me(
    token: str = Depends(oauth_schema), 
    deps: Dependencies = Depends()
):
    user = await deps.auth_service.get_user_from_token(token)
    return user
@router.patch("/me/update", response_model=UserRead)
async def update_my_profile(
    update_data: UserUpdate, 
    token: str = Depends(oauth2_scheme),
    deps: Dependencies = Depends(Dependencies)
):
    logger.info("User info update start")
    current_user = await deps.get_current_user(token)
    logger.info("current_data", extra = f"{current_user.username, current_user.email, current_user.updated_at, current_user.is_active, current_user.is_superuser}")
    logger.info("data_to_update", extra = update_data.model_dump())
    return await deps.auth_service.update_profile(current_user.id, update_data)
@router.get("/leaderboard", response_model=list[UserShort])
async def get_leaderboard(deps: Dependencies = Depends()):
    return await deps.user_repo.get_top_players(limit=10)
@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, deps : Dependencies = Depends(Dependencies)):
    logger.info("user_was_deleted", extra = f"{user_id=}")
    if await deps.auth_service.delete_user(user_id) == True:
        return status.HTTP_204_NO_CONTENT