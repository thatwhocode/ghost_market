from fastapi import APIRouter, Depends, HTTPException, Query, status
import uuid
from user_service.api.deps import Dependencies, admin_guard
from user_service.schemas.user import UserAdminView
from shared_packages.db.user import User
async def check_admin_access(deps: Dependencies = Depends(Dependencies)):
    await deps.get_current_admin()
router = APIRouter(prefix="/v1/admin", tags=["Admin"])

@router.get("/users", response_model=list[UserAdminView])
async def list_all_users(
    skip: int = 0,
    limit: int = 100,
    deps: Dependencies = Depends()):
    return await deps.user_repo.get_all_users(skip, limit)

@router.patch("/users/{user_id}/status", response_model=UserAdminView)
async def toggle_ban(
    user_id: uuid.UUID,
    is_active: bool,
    deps: Dependencies = Depends(Dependencies)):

    user = await deps.auth_service.toggle_user_status(user_id, is_active)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/{user_id}/reward", response_model=UserAdminView)
async def reward_user(
    user_id: uuid.UUID,
    echoes: int = Query(0),
    shards: int = Query(0),
    deps: Dependencies = Depends(Dependencies)):
    user = await deps.auth_service.apply_reward(user_id, echoes, shards)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/stats")
async def get_global_stats(
    deps: Dependencies = Depends(Dependencies)):
    return await deps.auth_service.get_stats()