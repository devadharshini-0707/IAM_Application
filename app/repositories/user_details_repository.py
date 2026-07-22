"""Data-access layer for the ``UserDetails`` aggregate.

Wraps a SQLAlchemy ``Session`` with typed methods scoped to the
``user_details`` table -- the one-to-one extended profile for a
``User``. Contains no business rules (profile completeness checks,
locale/timezone defaults, etc.); that judgment belongs to the service
layer above it.
"""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_details import UserDetails
from app.repositories.base_repository import BaseRepository


class UserDetailsRepository(BaseRepository[UserDetails, uuid.UUID]):
    """Typed CRUD and lookup methods for the ``UserDetails`` model."""

    model = UserDetails

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_id(self, user_details_id: uuid.UUID) -> Optional[UserDetails]:
        """Return the profile row with the given primary key, if any."""
        return self._session.get(UserDetails, user_details_id)

    def get_by_user_id(self, user_id: uuid.UUID) -> Optional[UserDetails]:
        """Return the profile belonging to the given user, if any."""
        stmt = select(UserDetails).where(UserDetails.user_id == user_id)
        return self._session.scalars(stmt).first()

    def exists_by_user_id(self, user_id: uuid.UUID) -> bool:
        """Return whether a profile row already exists for the given user."""
        stmt = select(UserDetails.user_details_id).where(UserDetails.user_id == user_id)
        return self._session.scalars(stmt).first() is not None
