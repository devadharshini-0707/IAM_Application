"""Data-access layer for the ``Identity`` aggregate.

Wraps a SQLAlchemy ``Session`` with typed methods scoped to the
``identities`` table -- the superclass row shared by every principal
(human user or service account). Contains no business rules (principal
type validation, status-transition rules, etc.); that judgment belongs
to the service layer above it.
"""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.identity import Identity
from app.repositories.base_repository import BaseRepository


class IdentityRepository(BaseRepository[Identity, uuid.UUID]):
    """Typed CRUD and lookup methods for the ``Identity`` model."""

    model = Identity

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_id(self, identity_id: uuid.UUID) -> Optional[Identity]:
        """Return the identity with the given primary key, if any."""
        return self._session.get(Identity, identity_id)

    def list_by_organization(
        self,
        organization_id: uuid.UUID,
        *,
        principal_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[Identity]:
        """Return identities scoped to an organization, optionally filtered
        by principal type and/or status."""
        stmt = select(Identity).where(Identity.organization_id == organization_id)
        if principal_type is not None:
            stmt = stmt.where(Identity.principal_type == principal_type)
        if status is not None:
            stmt = stmt.where(Identity.status == status)
        stmt = stmt.order_by(Identity.display_name)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        return list(self._session.scalars(stmt))
