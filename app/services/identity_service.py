"""Use-case layer for the ``Identity`` aggregate -- the abstract
superclass unifying every principal (human or service account) under a
single identity type.

Enforces the business rules ``IdentityRepository`` deliberately leaves
out (organization existence, recognized principal types) and owns the
transaction boundary around each use case. Depends only on
``IdentityRepository`` and ``OrganizationRepository``, never on
``sqlalchemy`` or a raw ``Session`` query.
"""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.identity import Identity
from app.repositories.identity_repository import IdentityRepository
from app.repositories.organization_repository import OrganizationRepository
from app.services.base_service import BaseService
from app.services.exceptions import ConflictError, NotFoundError, ValidationError


class IdentityService(BaseService):
    """Use cases for creating, looking up, and managing identities."""

    #: Principal types recognized by the platform -- human users and
    #: non-interactive service accounts, per ``Identity``'s docstring.
    ALLOWED_PRINCIPAL_TYPES = frozenset({"human", "service_account"})

    def __init__(
        self,
        session: Session,
        identity_repository: IdentityRepository,
        organization_repository: OrganizationRepository,
    ) -> None:
        super().__init__(session)
        self._identities = identity_repository
        self._organizations = organization_repository

    def create_identity(
        self,
        *,
        organization_id: uuid.UUID,
        principal_type: str,
        display_name: str,
        status: str = "active",
    ) -> Identity:
        """Create a new identity under the given organization.

        Raises:
            ValidationError: ``principal_type`` isn't a recognized value.
            NotFoundError: no organization exists with that id.
        """
        with self._transaction():
            if principal_type not in self.ALLOWED_PRINCIPAL_TYPES:
                raise ValidationError(
                    f"Unrecognized principal_type {principal_type!r}; expected "
                    f"one of {sorted(self.ALLOWED_PRINCIPAL_TYPES)}."
                )
            if self._organizations.get_by_id(organization_id) is None:
                raise NotFoundError(f"Organization {organization_id} does not exist.")
            identity = Identity(
                organization_id=organization_id,
                principal_type=principal_type,
                display_name=display_name,
                status=status,
            )
            return self._identities.add(identity)

    def get_identity(self, identity_id: uuid.UUID) -> Identity:
        """Return the identity with the given id.

        Raises:
            NotFoundError: no identity exists with that id.
        """
        identity = self._identities.get_by_id(identity_id)
        if identity is None:
            raise NotFoundError(f"Identity {identity_id} does not exist.")
        return identity

    def list_identities_by_organization(
        self,
        organization_id: uuid.UUID,
        *,
        principal_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[Identity]:
        """Return identities scoped to an organization, optionally filtered
        by principal type and/or status.

        Raises:
            NotFoundError: no organization exists with that id.
        """
        if self._organizations.get_by_id(organization_id) is None:
            raise NotFoundError(f"Organization {organization_id} does not exist.")
        return self._identities.list_by_organization(
            organization_id,
            principal_type=principal_type,
            status=status,
            limit=limit,
            offset=offset,
        )

    def rename_identity(self, identity_id: uuid.UUID, display_name: str) -> Identity:
        """Change an identity's display name.

        Raises:
            NotFoundError: no identity exists with that id.
        """
        with self._transaction():
            identity = self.get_identity(identity_id)
            identity.display_name = display_name
            return self._identities.update(identity)

    def update_identity_status(self, identity_id: uuid.UUID, status: str) -> Identity:
        """Transition an identity to a new status.

        Raises:
            NotFoundError: no identity exists with that id.
        """
        with self._transaction():
            identity = self.get_identity(identity_id)
            identity.status = status
            return self._identities.update(identity)

    def delete_identity(self, identity_id: uuid.UUID) -> None:
        """Delete an identity.

        Raises:
            NotFoundError: no identity exists with that id.
            ConflictError: the identity is still referenced by other
                records (e.g. a ``User`` specializing it).
        """
        with self._transaction():
            identity = self.get_identity(identity_id)
            self._delete_with_integrity_guard(
                self._identities,
                identity,
                conflict_message=(
                    f"Cannot delete identity {identity_id}: it is still "
                    "referenced by other records."
                ),
            )
