from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.services import get_user_service
from app.routes.security import get_current_user
from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
)
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.create_user(
        username=user_data.username,
        email=user_data.email,
        primary_organization_id=user_data.primary_organization_id,
    )


@router.get("/me", response_model=UserResponse)
def get_current_logged_in_user(
    current_user=Depends(get_current_user),
):
    return current_user


@router.get("/", response_model=list[UserResponse])
def get_users(
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_user(user_id)


# ---------- NEW UPDATE ENDPOINT ----------
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.update_user(
        user_id=user_id,
        username=user_data.username,
        email=user_data.email,
    )


@router.put("/{user_id}/enable", response_model=UserResponse)
def enable_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.enable_user(user_id)


@router.put("/{user_id}/disable", response_model=UserResponse)
def disable_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.disable_user(user_id)


@router.delete("/{user_id}")
def delete_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    user_service.delete_user(user_id)

    return {
        "message": "User deleted successfully."
    }