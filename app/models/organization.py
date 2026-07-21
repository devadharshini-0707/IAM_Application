"""ORGANIZATIONS -- the tenant boundary for the entire IAM platform."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.authentication_policy import AuthenticationPolicy
    from app.models.group import Group
    from app.models.identity import Identity
    from app.models.role import Role
    from app.models.user import User
    from app.models.user_audit_log import UserAuditLog
    from app.models.user_organization import UserOrganization


class Organization(Base, TimestampMixin):
    """A tenant in the multi-tenant IAM platform."""

    __tablename__ = "organizations"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    tier: Mapped[str] = mapped_column(String(30), nullable=False)
    parent_organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.organization_id"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    parent: Mapped[Optional["Organization"]] = relationship(
        "Organization",
        remote_side="Organization.organization_id",
        back_populates="children",
    )
    children: Mapped[list["Organization"]] = relationship(
        "Organization", back_populates="parent"
    )
    identities: Mapped[list["Identity"]] = relationship(
        "Identity",
        back_populates="organization",
        foreign_keys="Identity.organization_id",
    )
    primary_users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="primary_organization",
        foreign_keys="User.primary_organization_id",
    )
    user_memberships: Mapped[list["UserOrganization"]] = relationship(
        "UserOrganization",
        back_populates="organization",
        foreign_keys="UserOrganization.organization_id",
    )
    authentication_policy: Mapped[Optional["AuthenticationPolicy"]] = relationship(
        "AuthenticationPolicy", back_populates="organization", uselist=False
    )
    roles: Mapped[list["Role"]] = relationship("Role", back_populates="organization")
    groups: Mapped[list["Group"]] = relationship(
        "Group", back_populates="organization", foreign_keys="Group.organization_id"
    )
    audit_logs: Mapped[list["UserAuditLog"]] = relationship(
        "UserAuditLog",
        back_populates="organization",
        foreign_keys="UserAuditLog.organization_id",
    )

    def __repr__(self) -> str:
        return f"<Organization id={self.organization_id} slug={self.slug!r}>"