"""Authentication use cases."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.credential import Credential
from app.repositories.credential_repository import CredentialRepository
from app.repositories.user_repository import UserRepository
from app.services.exceptions import NotFoundError, ValidationError
from app.utils.jwt_handler import JWTHandler
from app.utils.password_hasher import PasswordHasher


class AuthService:
    """Handles user authentication."""

    def __init__(
        self,
        session: Session,
        user_repository: UserRepository,
        credential_repository: CredentialRepository,
        organization_service,
        identity_service,
        user_service,
        jwt_handler: JWTHandler,
    ) -> None:
        self._session = session
        self._users = user_repository
        self._credentials = credential_repository
        self._organization_service = organization_service
        self._identity_service = identity_service
        self._user_service = user_service
        self._jwt = jwt_handler

    def login(
        self,
        email: str,
        password: str,
    ) -> dict[str, str]:
        """Authenticate user and generate access token."""

        user = self._users.get_by_email(email)

        if user is None:
            raise NotFoundError(
                "Invalid email or password."
            )

        if user.status != "active":
            raise ValidationError(
                "User account is not active."
            )

        credential = self._credentials.get_active_password_credential(
            user.user_id
        )

        if credential is None:
            raise NotFoundError(
                "Password credential not found."
            )

        if not PasswordHasher.verify_password(
            password,
            credential.hash,
        ):
            raise ValidationError(
                "Invalid email or password."
            )

        token = self._jwt.create_access_token(
            subject=str(user.user_id),
            organization_id=str(user.primary_organization_id),
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    def signup(
        self,
        *,
        organization_name: str,
        organization_slug: str,
        username: str,
        email: str,
        password: str,
    ) -> dict[str, str]:
        """Register a new organization and its first user."""

        organization = self._organization_service.create_organization(
            name=organization_name,
            slug=organization_slug,
            tier="free",
        )

        identity = self._identity_service.create_identity(
            organization_id=organization.organization_id,
            principal_type="human",
            display_name=username,
        )

        user = self._user_service.create_user(
            identity_id=identity.identity_id,
            username=username,
            email=email,
            primary_organization_id=organization.organization_id,
        )

        credential = Credential(
            user_id=user.user_id,
            credential_type="password",
            hash=PasswordHasher.hash_password(password),
            algorithm="bcrypt",
            is_active=True,
        )

        self._credentials.create(credential)

        token = self._jwt.create_access_token(
            subject=str(user.user_id),
            organization_id=str(organization.organization_id),
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }
    