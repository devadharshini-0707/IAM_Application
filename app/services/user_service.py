from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.identity import Identity
from app.models.user import User
from app.repositories.identity_repository import IdentityRepository
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService
from app.services.exceptions import ConflictError, NotFoundError


class UserService(BaseService):
    """Business logic for User management."""

    def __init__(
        self,
        session: Session,
        user_repository: UserRepository,
        identity_repository: IdentityRepository,
        organization_repository: OrganizationRepository,
    ) -> None:
        super().__init__(session)
        self._users = user_repository
        self._identities = identity_repository
        self._organizations = organization_repository

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def create_user(
        self,
        *,
        username: str,
        email: str,
        primary_organization_id: uuid.UUID,
    ) -> User:
        """Create a new user and automatically create an Identity."""

        with self._transaction():

            if self._organizations.get_by_id(primary_organization_id) is None:
                raise NotFoundError(
                    f"Organization {primary_organization_id} does not exist."
                )

            if self._users.exists_by_username(username):
                raise ConflictError(
                    f"Username {username!r} is already taken."
                )

            if self._users.exists_by_email(email):
                raise ConflictError(
                    f"Email {email!r} is already registered."
                )

            identity = Identity(
                organization_id=primary_organization_id,
                principal_type="human",
                display_name=username,
                status="active",
            )

            self._session.add(identity)
            self._session.flush()

            user = User(
                identity_id=identity.identity_id,
                username=username,
                email=email,
                primary_organization_id=primary_organization_id,
                status="active",
            )

            return self._users.add(user)

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_all_users(self) -> list[User]:
        return self._users.get_all()

    def get_user(self, user_id: uuid.UUID) -> User:
        user = self._users.get_by_id(user_id)

        if user is None:
            raise NotFoundError("User not found.")

        return user

    def get_user_by_username(self, username: str) -> User:
        user = self._users.get_by_username(username)

        if user is None:
            raise NotFoundError("User not found.")

        return user

    def get_user_by_email(self, email: str) -> User:
        user = self._users.get_by_email(email)

        if user is None:
            raise NotFoundError("User not found.")

        return user

    def get_user_by_identity(self, identity_id: uuid.UUID) -> User:
        user = self._users.get_by_identity_id(identity_id)

        if user is None:
            raise NotFoundError("User not found.")

        return user

    def list_users_by_organization(
        self,
        organization_id: uuid.UUID,
        *,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[User]:

        return self._users.list_by_organization(
            organization_id,
            status=status,
            limit=limit,
            offset=offset,
        )

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update_user(
        self,
        *,
        user_id: uuid.UUID,
        username: str | None = None,
        email: str | None = None,
    ) -> User:
        """Update username and/or email."""

        with self._transaction():

            user = self.get_user(user_id)

            if username is not None and username != user.username:

                if self._users.exists_by_username(username):
                    raise ConflictError("Username already exists.")

                user.username = username

                if user.identity is not None:
                    user.identity.display_name = username

            if email is not None and email != user.email:

                if self._users.exists_by_email(email):
                    raise ConflictError("Email already exists.")

                user.email = email

            return self._users.update(user)

    def update_email(
        self,
        user_id: uuid.UUID,
        new_email: str,
    ) -> User:

        with self._transaction():

            user = self.get_user(user_id)

            if (
                new_email != user.email
                and self._users.exists_by_email(new_email)
            ):
                raise ConflictError("Email already exists.")

            user.email = new_email

            return self._users.update(user)

    def update_username(
        self,
        user_id: uuid.UUID,
        new_username: str,
    ) -> User:

        with self._transaction():

            user = self.get_user(user_id)

            if (
                new_username != user.username
                and self._users.exists_by_username(new_username)
            ):
                raise ConflictError("Username already exists.")

            user.username = new_username

            return self._users.update(user)

    def enable_user(
        self,
        user_id: uuid.UUID,
    ) -> User:

        with self._transaction():

            user = self.get_user(user_id)

            user.status = "active"

            return self._users.update(user)

    def disable_user(
        self,
        user_id: uuid.UUID,
    ) -> User:

        with self._transaction():

            user = self.get_user(user_id)

            user.status = "disabled"

            return self._users.update(user)

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete_user(
        self,
        user_id: uuid.UUID,
    ) -> User:

        with self._transaction():

            user = self.get_user(user_id)

            # Soft delete
            user.status = "deleted"

            if user.identity is not None:
                user.identity.status = "deleted"

            return self._users.update(user)