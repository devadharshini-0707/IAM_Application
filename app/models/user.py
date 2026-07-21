"""USERS -- specializes IDENTITIES with login-specific attributes for human
principals only.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.credential import Credential
    from app.models.identity import Identity
    from app.models.mfa_factor import MfaFactor
    from app.models.organization import Organization
    from app.models.user_details import UserDetails
    from app.models.user_group import UserGroup
    from app.models.user_organization import UserOrganization
    from app.models.user_role import UserRole


class User(Base, TimestampMixin):
    """A login-capable human user, specializing an ``Identity`` row."""

    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    identity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("identities.identity_id"),
        nullable=False,
        unique=True,
    )
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    primary_organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.organization_id"),
        nullable=False,
    )

    identity: Mapped["Identity"] = relationship("Identity", back_populates="user")
    primary_organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="primary_users",
        foreign_keys=[primary_organization_id],
    )
    details: Mapped["UserDetails"] = relationship(
        "UserDetails", back_populates="user", uselist=False
    )
    organization_memberships: Mapped[list["UserOrganization"]] = relationship(
        "UserOrganization",
        back_populates="user",
        foreign_keys="UserOrganization.user_id",
    )
    credentials: Mapped[list["Credential"]] = relationship(
        "Credential", back_populates="user"
    )
    mfa_factors: Mapped[list["MfaFactor"]] = relationship(
        "MfaFactor", back_populates="user"
    )
    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole", back_populates="user", foreign_keys="UserRole.user_id"
    )
    user_groups: Mapped[list["UserGroup"]] = relationship(
        "UserGroup", back_populates="user", foreign_keys="UserGroup.user_id"
    )

    def __repr__(self) -> str:
        return f"<User id={self.user_id} username={self.username!r}>"