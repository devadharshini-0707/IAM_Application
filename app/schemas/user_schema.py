from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """
    Request body for creating a user.

    Identity is created automatically by the backend.
    """

    username: str
    email: EmailStr
    primary_organization_id: UUID


class UserUpdate(BaseModel):
    """
    Request body for updating a user.
    """

    username: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    """
    Response returned by the User API.
    """

    user_id: UUID
    identity_id: UUID
    username: str
    email: EmailStr
    status: str
    primary_organization_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)