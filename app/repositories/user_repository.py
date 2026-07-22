"""Data-access layer for the ``User`` aggregate.

Wraps a SQLAlchemy ``Session`` with typed methods scoped to the ``users``
table -- the login-capable specialization of ``Identity``. Contains no
business rules (credential handling, status-transition rules, uniqueness
enforcement, etc.); that judgment belongs to the service layer above it.
The ``exists_by_*`` helpers below return a plain boolean from a query --
they are a data-access convenience, not a validation decision.
"""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User, uuid.UUID]):
    """Typed CRUD and lookup methods for the ``User`` model."""

    model = User

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Return the user with the given primary key, if any."""
        return self._session.get(User, user_id)

    def get_by_identity_id(self, identity_id: uuid.UUID) -> Optional[User]:
        """Return the user specializing the given identity, if any."""
        stmt = select(User).where(User.identity_id == identity_id)
        return self._session.scalars(stmt).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Return the user with the given unique username, if any."""
        stmt = select(User).where(User.username == username)
        return self._session.scalars(stmt).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Return the user with the given unique email address, if any."""
        stmt = select(User).where(User.email == email)
        return self._session.scalars(stmt).first()

    def exists_by_username(self, username: str) -> bool:
        """Return whether a user with the given username exists."""
        stmt = select(User.user_id).where(User.username == username)
        return self._session.scalars(stmt).first() is not None

    def exists_by_email(self, email: str) -> bool:
        """Return whether a user with the given email address exists."""
        stmt = select(User.user_id).where(User.email == email)
        return self._session.scalars(stmt).first() is not None

    def list_by_organization(
        self,
        organization_id: uuid.UUID,
        *,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[User]:
        """Return users whose primary organization matches the given id,
        optionally filtered by status."""
        stmt = select(User).where(User.primary_organization_id == organization_id)
        if status is not None:
            stmt = stmt.where(User.status == status)
        stmt = stmt.order_by(User.username)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        return list(self._session.scalars(stmt))
