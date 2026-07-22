"""Data-access layer for the ``Organization`` aggregate.

Wraps a SQLAlchemy ``Session`` with typed methods scoped to the
``organizations`` table. This repository only translates a request for
data into a query and back -- it enforces no business rules (slug
formatting, tier validation, status transitions, tenant hierarchy
depth, etc.); that judgment belongs to the service layer above it.
"""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.repositories.base_repository import BaseRepository


class OrganizationRepository(BaseRepository[Organization, uuid.UUID]):
    """Typed CRUD and lookup methods for the ``Organization`` model."""

    model = Organization

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_id(self, organization_id: uuid.UUID) -> Optional[Organization]:
        """Return the organization with the given primary key, if any."""
        return self._session.get(Organization, organization_id)

    def get_by_slug(self, slug: str) -> Optional[Organization]:
        """Return the organization with the given unique slug, if any."""
        stmt = select(Organization).where(Organization.slug == slug)
        return self._session.scalars(stmt).first()

    def exists_by_slug(self, slug: str) -> bool:
        """Return whether an organization with the given slug exists."""
        stmt = select(Organization.organization_id).where(Organization.slug == slug)
        return self._session.scalars(stmt).first() is not None

    def list_children(self, parent_organization_id: uuid.UUID) -> list[Organization]:
        """Return the direct child organizations of the given parent."""
        stmt = (
            select(Organization)
            .where(Organization.parent_organization_id == parent_organization_id)
            .order_by(Organization.name)
        )
        return list(self._session.scalars(stmt))

    def list_by_status(
        self,
        status: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[Organization]:
        """Return organizations with the given status, oldest first."""
        stmt = (
            select(Organization)
            .where(Organization.status == status)
            .order_by(Organization.created_at)
        )
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        return list(self._session.scalars(stmt))
