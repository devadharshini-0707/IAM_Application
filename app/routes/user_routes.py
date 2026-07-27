from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.services import get_user_service
from app.routes.security import get_current_user
from app.schemas.user_schema import UserCreate, UserResponse
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
        identity_id=user_data.identity_id,
        username=user_data.username,
        email=user_data.email,
        primary_organization_id=user_data.primary_organization_id,
    )


# Keep this BEFORE /{user_id}
@router.get("/me")
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