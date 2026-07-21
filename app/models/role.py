"""ROLES -- the set of named, tenant-scoped roles available for assignment."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user_role import UserRole


class Role(Base, TimestampMixin):
    """A tenant-scoped role available for assignment to users.

    Maps to the ``ROLES`` table. ``role_code`` is unique per organization,
    not globally, per the PDF.
    """

    __tablename__ = "roles"
    __table_args__ = (
        UniqueConstraint("organization_id", "role_code", name="uq_roles_org_code"),
    )

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.organization_id"), nullable=False
    )
    role_name: Mapped[str] = mapped_column(String(150), nullable=False)
    role_code: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_system_role: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="roles"
    )
    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole", back_populates="role", foreign_keys="UserRole.role_id"
    )

    def __repr__(self) -> str:
        return f"<Role id={self.role_id} code={self.role_code!r}>"