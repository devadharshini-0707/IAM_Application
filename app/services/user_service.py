from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models.identity import Identity
from app.models.user import User
from app.repositories.credential_repository import CredentialRepository
from app.repositories.identity_repository import IdentityRepository
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService
from app.services.exceptions import ConflictError, NotFoundError


class UserService(BaseService):
    """Use cases for creating, looking up, updating and soft deleting users."""

    def __init__(
        self,
        session: Session,
        user_repository: UserRepository,
        identity_repository: IdentityRepository,
        organization_repository: OrganizationRepository,
        credential_repository: CredentialRepository,
    ) -> None:
        super().__init__(session)

        self._users = user_repository
        self._identities = identity_repository
        self._organizations = organization_repository
        self._credentials = credential_repository

    def create_user(
        self,
        *,
        username: str,
        email: str,
        primary_organization_id: uuid.UUID,
    ) -> User:

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

            identity = self._identities.add(identity)

            user = User(
                identity_id=identity.identity_id,
                username=username,
                email=email,
                primary_organization_id=primary_organization_id,
                status="active",
            )

            return self._users.add(user)

    def get_all_users(self) -> list[User]:
        return self._users.get_all()

    def search_users(
        self,
        keyword: str,
    ) -> list[User]:
        return self._users.search(keyword)

    def get_users_paginated(
        self,
        *,
        page: int,
        page_size: int,
    ) -> list[User]:
        offset = (page - 1) * page_size

        return self._users.get_paginated(
            limit=page_size,
            offset=offset,
        )

    def get_user(
        self,
        user_id: uuid.UUID,
    ) -> User:
        user = self._users.get_by_id(user_id)

        if user is None:
            raise NotFoundError(
                f"User {user_id} does not exist."
            )

        return user

    def get_user_by_username(
        self,
        username: str,
    ) -> User:
        user = self._users.get_by_username(username)

        if user is None:
            raise NotFoundError(
                f"User with username {username!r} does not exist."
            )

        return user

    def get_user_by_email(
        self,
        email: str,
    ) -> User:
        user = self._users.get_by_email(email)

        if user is None:
            raise NotFoundError(
                f"User with email {email!r} does not exist."
            )

        return user
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
                raise ConflictError(
                    f"Email {new_email!r} is already registered."
                )

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
                raise ConflictError(
                    f"Username {new_username!r} is already taken."
                )

            user.username = new_username

            identity = self._identities.get_by_id(
                user.identity_id
            )

            if identity is not None:
                identity.display_name = new_username
                self._identities.update(identity)

            return self._users.update(user)

    def update_status(
        self,
        user_id: uuid.UUID,
        status: str,
    ) -> User:

        with self._transaction():

            user = self.get_user(user_id)

            user.status = status

            identity = self._identities.get_by_id(
                user.identity_id
            )

            if identity is not None:
                identity.status = status
                self._identities.update(identity)

            return self._users.update(user)

    def delete_user(
        self,
        user_id: uuid.UUID,
    ) -> None:

        with self._transaction():

            user = self.get_user(user_id)

            user.status = "deleted"
            self._users.update(user)

            identity = self._identities.get_by_id(
                user.identity_id
            )

            if identity is not None:
                identity.status = "deleted"
                self._identities.update(identity)

            credentials = self._credentials.get_by_user(
                user.user_id
            )

            for credential in credentials:
                credential.is_active = False
                self._credentials.update(credential)