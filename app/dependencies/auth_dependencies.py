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

    organization_repository = OrganizationRepository(session)
    identity_repository = IdentityRepository(session)
    user_repository = UserRepository(session)
    credential_repository = CredentialRepository(session)

    organization_service = OrganizationService(
        session=session,
        organization_repository=organization_repository,
    )

    identity_service = IdentityService(
        session=session,
        identity_repository=identity_repository,
        organization_repository=organization_repository,
    )

    user_service = UserService(
        session=session,
        user_repository=user_repository,
        identity_repository=identity_repository,
        organization_repository=organization_repository,
        credential_repository=credential_repository,
    )

    return AuthService(
        session=session,
        user_repository=user_repository,
        credential_repository=credential_repository,
        organization_service=organization_service,
        user_service=user_service,
        jwt_handler=JWTHandler(),
    )