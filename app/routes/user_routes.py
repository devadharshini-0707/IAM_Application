from uuid import UUID

from fastapi import APIRouter, Depends

from app.schemas.user_schema import UserCreate, UserResponse
from app.dependencies.services import get_user_service
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.create_user(
        identity_id=user_data.identity_id,
        username=user_data.username,
        email=user_data.email,
        status=user_data.status,
        primary_organization_id=user_data.primary_organization_id,
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_user(user_id)