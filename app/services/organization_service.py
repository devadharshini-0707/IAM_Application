"""Use-case layer for the ``Organization`` aggregate -- the tenant
boundary for the entire IAM platform.

Enforces the business rules ``OrganizationRepository`` deliberately
leaves out (slug uniqueness, parent-organization existence, self-
parenting, deleting a tenant that still has children) and owns the
transaction boundary around each use case. Depends only on
``OrganizationRepository``, never on ``sqlalchemy`` or a raw ``Session``
query.
"""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.repositories.organization_repository import OrganizationRepository
from app.services.base_service import BaseService
from app.services.exceptions import ConflictError, NotFoundError, ValidationError


class OrganizationService(BaseService):
    """Use cases for creating, looking up, and managing organizations."""

    def __init__(
        self,
        session: Session,
        organization_repository: OrganizationRepository,
    ) -> None:
        super().__init__(session)
        self._organizations = organization_repository

    def create_organization(
        self,
        *,
        name: str,
        slug: str,
        tier: str,
        status: str = "active",
        parent_organization_id: Optional[uuid.UUID] = None,
    ) -> Organization:
        """Create a new organization.

        Raises:
            ConflictError: ``slug`` is already taken by another organization.
            NotFoundError: ``parent_organization_id`` was given but no such
                organization exists.
        """
        with self._transaction():
            if self._organizations.exists_by_slug(slug):
                raise ConflictError(f"An organization with slug {slug!r} already exists.")
            if (
                parent_organization_id is not None
                and self._organizations.get_by_id(parent_organization_id) is None
            ):
                raise NotFoundError(
                    f"Parent organization {parent_organization_id} does not exist."
                )
            organization = Organization(
                name=name,
                slug=slug,
                tier=tier,
                status=status,
                parent_organization_id=parent_organization_id,
            )
            return self._organizations.add(organization)

    def get_organization(self, organization_id: uuid.UUID) -> Organization:
        """Return the organization with the given id.

        Raises:
            NotFoundError: no organization exists with that id.
        """
        organization = self._organizations.get_by_id(organization_id)
        if organization is None:
            raise NotFoundError(f"Organization {organization_id} does not exist.")
        return organization

    def get_organization_by_slug(self, slug: str) -> Organization:
        """Return the organization with the given unique slug.

        Raises:
            NotFoundError: no organization exists with that slug.
        """
        organization = self._organizations.get_by_slug(slug)
        if organization is None:
            raise NotFoundError(f"Organization with slug {slug!r} does not exist.")
        return organization

    def list_child_organizations(
        self, parent_organization_id: uuid.UUID
    ) -> list[Organization]:
        """Return the direct children of the given organization.

        Raises:
            NotFoundError: no organization exists with that id.
        """
        self.get_organization(parent_organization_id)
        return self._organizations.list_children(parent_organization_id)

    def list_organizations_by_status(
        self,
        status: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[Organization]:
        """Return organizations with the given status, oldest first."""
        return self._organizations.list_by_status(status, limit=limit, offset=offset)

    def rename_organization(self, organization_id: uuid.UUID, name: str) -> Organization:
        """Change an organization's display name.

        Raises:
            NotFoundError: no organization exists with that id.
        """
        with self._transaction():
            organization = self.get_organization(organization_id)
            organization.name = name
            return self._organizations.update(organization)

    def update_organization_status(
        self, organization_id: uuid.UUID, status: str
    ) -> Organization:
        """Transition an organization to a new status.

        Raises:
            NotFoundError: no organization exists with that id.
        """
        with self._transaction():
            organization = self.get_organization(organization_id)
            organization.status = status
            return self._organizations.update(organization)

    def reparent_organization(
        self,
        organization_id: uuid.UUID,
        new_parent_organization_id: Optional[uuid.UUID],
    ) -> Organization:
        """Move an organization under a different parent, or detach it from
        its parent entirely when ``new_parent_organization_id`` is ``None``.

        Raises:
            ValidationError: ``new_parent_organization_id`` is the
                organization's own id.
            NotFoundError: the organization, or the new parent, does not
                exist.
        """
        with self._transaction():
            if organization_id == new_parent_organization_id:
                raise ValidationError("An organization cannot be its own parent.")
            organization = self.get_organization(organization_id)
            if new_parent_organization_id is not None:
                self.get_organization(new_parent_organization_id)
            organization.parent_organization_id = new_parent_organization_id
            return self._organizations.update(organization)

    def delete_organization(self, organization_id: uuid.UUID) -> None:
        """Delete an organization.

        Raises:
            NotFoundError: no organization exists with that id.
            ConflictError: the organization still has child organizations,
                or is still referenced by other records.
        """
        with self._transaction():
            organization = self.get_organization(organization_id)
            if self._organizations.list_children(organization_id):
                raise ConflictError(
                    f"Cannot delete organization {organization_id}: it still has "
                    "child organizations."
                )
            self._delete_with_integrity_guard(
                self._organizations,
                organization,
                conflict_message=(
                    f"Cannot delete organization {organization_id}: it is still "
                    "referenced by other records."
                ),
            )
