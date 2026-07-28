"""Data-access layer for the User aggregate."""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User, uuid.UUID]):
    """Repository for User."""

    model = User

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_all(self) -> list[User]:
        return (
            self._session.query(User)
            .filter(User.status != "deleted")
            .order_by(User.username)
            .all()
        )

    def get_paginated(
        self,
        *,
        limit: int,
        offset: int,
        search: str | None = None,
    ) -> tuple[list[User], int]:
        """
        Returns (users, total_count)
        """

        query = (
            self._session.query(User)
            .filter(User.status != "deleted")
        )

        if search:
            query = query.filter(
                or_(
                    User.username.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                )
            )

        total = query.count()

        users = (
            query.order_by(User.username)
            .offset(offset)
            .limit(limit)
            .all()
        )

        return users, total

    def get_by_id(
        self,
        user_id: uuid.UUID,
    ) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.user_id == user_id)
            .where(User.status != "deleted")
        )

        return self._session.scalars(stmt).first()

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
        stmt = (
            select(User)
            .where(User.username == username)
            .where(User.status != "deleted")
        )

        return self._session.scalars(stmt).first()

    def get_by_email(
        self,
        email: str,
    ) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.email == email)
            .where(User.status != "deleted")
        )

        return self._session.scalars(stmt).first()

    def exists_by_username(
        self,
        username: str,
    ) -> bool:
        stmt = (
            select(User.user_id)
            .where(User.username == username)
            .where(User.status != "deleted")
        )

        return self._session.scalars(stmt).first() is not None

    def exists_by_email(
        self,
        email: str,
    ) -> bool:
        stmt = (
            select(User.user_id)
            .where(User.email == email)
            .where(User.status != "deleted")
        )

        return self._session.scalars(stmt).first() is not None

    def update(
        self,
        user: User,
    ) -> User:
        self._session.add(user)
        self._session.flush()
        self._session.refresh(user)
        return user

    def enable(
        self,
        user: User,
    ) -> User:
        user.status = "active"
        return self.update(user)

    def disable(
        self,
        user: User,
    ) -> User:
        user.status = "disabled"
        return self.update(user)

    def soft_delete(
        self,
        user: User,
    ) -> User:
        user.status = "deleted"
        return self.update(user)

    def search(
        self,
        keyword: str,
    ) -> list[User]:

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
        status: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[User]:

        stmt = (
            select(User)
            .where(
                User.primary_organization_id == organization_id
            )
            .where(User.status != "deleted")
        )

        if status:
            stmt = stmt.where(User.status == status)

        stmt = stmt.order_by(User.username)

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        return list(
            self._session.scalars(stmt)
        )