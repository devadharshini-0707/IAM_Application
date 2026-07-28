from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    primary_organization_id: UUID


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    user_id: UUID
    identity_id: UUID
    username: str
    email: EmailStr
    status: str
    primary_organization_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)