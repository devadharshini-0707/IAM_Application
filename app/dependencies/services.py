from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db

from app.repositories.user_repository import UserRepository
from app.repositories.identity_repository import IdentityRepository
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.credential_repository import CredentialRepository

from app.services.user_service import UserService


def get_user_service(
    session: Session = Depends(get_db),
) -> UserService:
    return UserService(
        session=session,
        user_repository=UserRepository(session),
        identity_repository=IdentityRepository(session),
        organization_repository=OrganizationRepository(session),
        credential_repository=CredentialRepository(session),
    )