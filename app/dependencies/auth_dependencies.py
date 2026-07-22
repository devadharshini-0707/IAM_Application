from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.repositories.organization_repository import OrganizationRepository
from app.repositories.identity_repository import IdentityRepository
from app.repositories.user_repository import UserRepository
from app.repositories.credential_repository import CredentialRepository

from app.services.organization_service import OrganizationService
from app.services.identity_service import IdentityService
from app.services.user_service import UserService
from app.services.auth_service import AuthService

from app.utils.jwt_handler import JWTHandler


def get_auth_service(
    session: Session = Depends(get_db),
) -> AuthService:

    organization_service = OrganizationService(
        session=session,
        organization_repository=OrganizationRepository(session),
    )

    identity_service = IdentityService(
        session=session,
        identity_repository=IdentityRepository(session),
        organization_repository=OrganizationRepository(session),
    )

    user_service = UserService(
        session=session,
        user_repository=UserRepository(session),
        identity_repository=IdentityRepository(session),
        organization_repository=OrganizationRepository(session),
    )

    return AuthService(
        session=session,
        organization_service=organization_service,
        identity_service=identity_service,
        user_service=user_service,
        credential_repository=CredentialRepository(session),
        jwt_handler=JWTHandler(),
    )