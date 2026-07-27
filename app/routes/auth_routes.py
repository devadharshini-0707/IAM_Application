from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth_dependencies import get_auth_service
from app.schemas.auth_schema import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
)
from app.services.auth_service import AuthService
from app.services.exceptions import ConflictError

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=TokenResponse,
)
def signup(
    request: SignupRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        token = auth_service.signup(
            organization_name=request.organization_name,
            organization_slug=request.organization_slug,
            username=request.username,
            email=request.email,
            password=request.password,
        )
        return TokenResponse(**token)

    except ConflictError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    except Exception:
        import traceback
        traceback.print_exc()
        raise


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    token = auth_service.login(
        email=request.email,
        password=request.password,
    )

    return TokenResponse(**token)