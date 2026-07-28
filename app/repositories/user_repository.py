"""Data-access layer for the ``User`` aggregate.

Wraps a SQLAlchemy ``Session`` with typed methods scoped to the ``users``
table -- the login-capable specialization of ``Identity``. Contains no
business rules (credential handling, status-transition rules, uniqueness
enforcement, etc.); that judgment belongs to the service layer above it.
"""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User, uuid.UUID]):
    """Typed CRUD and lookup methods for the ``User`` model."""

    model = User

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_all(self) -> list[User]:
        """
        Return all active/non-deleted users ordered by username.
        """

        return (
            self._session.query(User)
            .filter(User.status != "deleted")
            .order_by(User.username)
            .all()
        )

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self._session.get(User, user_id)

    def get_by_identity_id(
        self,
        identity_id: uuid.UUID,
    ) -> Optional[User]:
        stmt = select(User).where(
            User.identity_id == identity_id
        )
        return self._session.scalars(stmt).first()

    def get_by_username(
        self,
        username: str,
    ) -> Optional[User]:
        stmt = select(User).where(
            User.username == username
        )
        return self._session.scalars(stmt).first()

    def get_by_email(
        self,
        email: str,
    ) -> Optional[User]:
        stmt = select(User).where(
            User.email == email
        )
        return self._session.scalars(stmt).first()

    def exists_by_username(
        self,
        username: str,
    ) -> bool:
        stmt = select(User.user_id).where(
            User.username == username
        )
        return self._session.scalars(stmt).first() is not None

    def exists_by_email(
        self,
        email: str,
    ) -> bool:
        stmt = select(User.user_id).where(
            User.email == email
        )
        return self._session.scalars(stmt).first() is not None

    def update(
        self,
        user: User,
    ) -> User:
        self._session.add(user)
        self._session.flush()
        return user

    def enable(
        self,
        user: User,
    ) -> User:
        user.status = "active"
        self._session.add(user)
        self._session.flush()
        return user

    def disable(
        self,
        user: User,
    ) -> User:
        user.status = "disabled"
        self._session.add(user)
        self._session.flush()
        return user

    def soft_delete(
        self,
        user: User,
    ) -> User:
        """
        Soft delete instead of removing the row.
        """

        user.status = "deleted"

        self._session.add(user)
        self._session.flush()

        return user

    def search(
        self,
        keyword: str,
    ) -> list[User]:
        """
        Search users by username or email.
        """

        stmt = (
            select(User)
            .where(User.status != "deleted")
            .where(
                or_(
                    User.username.ilike(f"%{keyword}%"),
                    User.email.ilike(f"%{keyword}%"),
                )
            )
            .order_by(User.username)
        )

        return list(
            self._session.scalars(stmt)
        )

    def list_by_organization(
        self,
        organization_id: uuid.UUID,
        *,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[User]:

        stmt = (
            select(User)
            .where(
                User.primary_organization_id == organization_id
            )
            .where(User.status != "deleted")
        )

        if status is not None:
            stmt = stmt.where(
                User.status == status
            )

        stmt = stmt.order_by(User.username)

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        return list(
            self._session.scalars(stmt)
        )