from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


# Request body for creating a user
class UserCreate(BaseModel):
    identity_id: UUID
    username: str
    email: EmailStr
    primary_organization_id: UUID


# Request body for updating a user
class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    


# Response returned by API
class UserResponse(BaseModel):
    user_id: UUID
    identity_id: UUID
    username: str
    email: EmailStr
    primary_organization_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)