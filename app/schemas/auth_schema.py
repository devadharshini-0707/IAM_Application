from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    """Request body for user registration."""

    organization_name: str
    organization_slug: str

    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """Request body for user login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token returned after successful authentication."""

    access_token: str
    token_type: str = "bearer"