"""Use-case layer for the ``User`` aggregate -- the login-capable
specialization of ``Identity``.

Enforces the business rules ``UserRepository`` deliberately leaves out
(identity and organization existence, the one-to-one link between a
``User`` and its ``Identity``, username/email uniqueness) and owns the
transaction boundary around each use case. Depends only on
``UserRepository``, ``IdentityRepository``, and
``OrganizationRepository``, never on ``sqlalchemy`` or a raw ``Session``
query.
"""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.identity_repository import IdentityRepository
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService
from app.services.exceptions import ConflictError, NotFoundError


class UserService(BaseService):
    """Use cases for creating, looking up, and managing login-capable users."""

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

    def create_user(
        self,
        *,
        identity_id: uuid.UUID,
        username: str,
        email: str,
        primary_organization_id: uuid.UUID,
        status: str = "active",
    ) -> User:
        """Create a new user specializing an existing identity.

        Raises:
            NotFoundError: the identity or the primary organization does
                not exist.
            ConflictError: the identity already has an associated user, or
                ``username``/``email`` is already taken.
        """
        with self._transaction():
            if self._identities.get_by_id(identity_id) is None:
                raise NotFoundError(f"Identity {identity_id} does not exist.")
            if self._users.get_by_identity_id(identity_id) is not None:
                raise ConflictError(
                    f"Identity {identity_id} already has an associated user."
                )
            if self._organizations.get_by_id(primary_organization_id) is None:
                raise NotFoundError(
                    f"Organization {primary_organization_id} does not exist."
                )
            if self._users.exists_by_username(username):
                raise ConflictError(f"Username {username!r} is already taken.")
            if self._users.exists_by_email(email):
                raise ConflictError(f"Email {email!r} is already registered.")
            user = User(
                identity_id=identity_id,
                username=username,
                email=email,
                primary_organization_id=primary_organization_id,
                status=status,
            )
            return self._users.add(user)

    def get_user(self, user_id: uuid.UUID) -> User:
        """Return the user with the given id.

        Raises:
            NotFoundError: no user exists with that id.
        """
        user = self._users.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} does not exist.")
        return user

    def get_user_by_username(self, username: str) -> User:
        """Return the user with the given unique username.

        Raises:
            NotFoundError: no user exists with that username.
        """
        user = self._users.get_by_username(username)
        if user is None:
            raise NotFoundError(f"User with username {username!r} does not exist.")
        return user

    def get_user_by_email(self, email: str) -> User:
        """Return the user with the given unique email address.

        Raises:
            NotFoundError: no user exists with that email address.
        """
        user = self._users.get_by_email(email)
        if user is None:
            raise NotFoundError(f"User with email {email!r} does not exist.")
        return user

    def get_user_by_identity(self, identity_id: uuid.UUID) -> User:
        """Return the user specializing the given identity.

        Raises:
            NotFoundError: no user is associated with that identity.
        """
        user = self._users.get_by_identity_id(identity_id)
        if user is None:
            raise NotFoundError(f"Identity {identity_id} has no associated user.")
        return user

    def list_users_by_organization(
        self,
        organization_id: uuid.UUID,
        *,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[User]:
        """Return users whose primary organization matches the given id,
        optionally filtered by status.

        Raises:
            NotFoundError: no organization exists with that id.
        """
        if self._organizations.get_by_id(organization_id) is None:
            raise NotFoundError(f"Organization {organization_id} does not exist.")
        return self._users.list_by_organization(
            organization_id, status=status, limit=limit, offset=offset
        )

    def update_email(self, user_id: uuid.UUID, new_email: str) -> User:
        """Change a user's email address.

        Raises:
            NotFoundError: no user exists with that id.
            ConflictError: ``new_email`` is already registered to a
                different user.
        """
        with self._transaction():
            user = self.get_user(user_id)
            if new_email != user.email and self._users.exists_by_email(new_email):
                raise ConflictError(f"Email {new_email!r} is already registered.")
            user.email = new_email
            return self._users.update(user)

    def update_username(self, user_id: uuid.UUID, new_username: str) -> User:
        """Change a user's username.

        Raises:
            NotFoundError: no user exists with that id.
            ConflictError: ``new_username`` is already taken by a different
                user.
        """
        with self._transaction():
            user = self.get_user(user_id)
            if new_username != user.username and self._users.exists_by_username(
                new_username
            ):
                raise ConflictError(f"Username {new_username!r} is already taken.")
            user.username = new_username
            return self._users.update(user)

    def update_status(self, user_id: uuid.UUID, status: str) -> User:
        """Transition a user to a new status.

        Raises:
            NotFoundError: no user exists with that id.
        """
        with self._transaction():
            user = self.get_user(user_id)
            user.status = status
            return self._users.update(user)

    def transfer_primary_organization(
        self, user_id: uuid.UUID, new_organization_id: uuid.UUID
    ) -> User:
        """Move a user's primary organization membership to a different
        organization.

        Raises:
            NotFoundError: the user, or the new organization, does not
                exist.
        """
        with self._transaction():
            user = self.get_user(user_id)
            if self._organizations.get_by_id(new_organization_id) is None:
                raise NotFoundError(
                    f"Organization {new_organization_id} does not exist."
                )
            user.primary_organization_id = new_organization_id
            return self._users.update(user)

    def delete_user(self, user_id: uuid.UUID) -> None:
        """Delete a user.

        Raises:
            NotFoundError: no user exists with that id.
            ConflictError: the user is still referenced by other records
                (e.g. credentials, MFA factors, role or group memberships).
        """
        with self._transaction():
            user = self.get_user(user_id)
            self._delete_with_integrity_guard(
                self._users,
                user,
                conflict_message=(
                    f"Cannot delete user {user_id}: it is still referenced by "
                    "other records."
                ),
            )
