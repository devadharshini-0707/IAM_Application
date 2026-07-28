from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.dependencies.services import get_user_service
from app.routes.security import get_current_user
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
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


@router.get("/me")
def get_current_logged_in_user(
    current_user=Depends(get_current_user),
):
    return current_user


@router.get("/")
def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    user_service: UserService = Depends(get_user_service),
):
    users, total = user_service.get_users_paginated(
        page=page,
        page_size=page_size,
        search=search,
    )

    return {
        "items": users,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (
            (total + page_size - 1) // page_size
        ),
    }


@router.get("/search", response_model=list[UserResponse])
def search_users(
    keyword: str,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.search_users(keyword)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.get_user(user_id)

    if user_data.username is not None:
        user = user_service.update_username(
            user_id,
            user_data.username,
        )

    if user_data.email is not None:
        user = user_service.update_email(
            user_id,
            user_data.email,
        )

    return user


@router.put("/{user_id}/enable", response_model=UserResponse)
def enable_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.update_status(
        user_id=user_id,
        status="active",
    )


@router.put("/{user_id}/disable", response_model=UserResponse)
def disable_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.update_status(
        user_id=user_id,
        status="disabled",
    )


@router.delete("/{user_id}")
def delete_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    user_service.delete_user(user_id)

    return {
        "message": "User deleted successfully."
    }