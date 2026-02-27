# user_service/api/admin.py
from fastapi import APIRouter, Depends, HTTPException, Query
import uuid
from user_service.api.deps import Dependencies
from user_service.schemas.user import UserAdminView
from shared_packages.db import User
router = APIRouter(prefix="/v1/admin", tags=["Admin"])

@router.get("/users", response_model=list[UserAdminView])
async def list_all_users(
    skip: int = 0,
    limit: int = 100,
    deps: Dependencies = Depends(),
    admin: User = Depends(Dependencies.get_current_admin)
):
    return await deps.user_repo.get_all_users(skip, limit)

@router.patch("/users/{user_id}/status", response_model=UserAdminView)
async def toggle_ban(
    user_id: uuid.UUID,
    is_active: bool,
    deps: Dependencies = Depends(),
    admin: User = Depends(Dependencies.get_current_admin)
):
    user = await deps.auth_service.toggle_user_status(user_id, {"is_active": is_active})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/{user_id}/reward", response_model=UserAdminView)
async def reward_user(
    user_id: uuid.UUID,
    echoes: int = Query(0),
    shards: int = Query(0),
    deps: Dependencies = Depends(),
    admin: User = Depends(Dependencies.get_current_admin)
):
    """Додати валюту гравцю (можна від'ємні значення для штрафів)"""
    user = await deps.user_repo.adjust_user_balance(user_id, echoes, shards)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/stats")
async def get_global_stats(
    deps: Dependencies = Depends(),
    admin: User = Depends(Dependencies.get_current_admin)
):
    return await deps.auth_service.get_stats()