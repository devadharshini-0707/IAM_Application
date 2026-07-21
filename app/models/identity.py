"""IDENTITIES -- the abstract superclass unifying every principal (human or
service account) under a single identity type.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user import User
    from app.models.user_audit_log import UserAuditLog


class Identity(Base, TimestampMixin):
    """A principal in the system -- human user or service account."""

    __tablename__ = "identities"

    identity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.organization_id"),
        nullable=False,
    )
    principal_type: Mapped[str] = mapped_column(String(20), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="identities", foreign_keys=[organization_id]
    )
    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="identity", uselist=False
    )
    audit_logs: Mapped[list["UserAuditLog"]] = relationship(
        "UserAuditLog",
        back_populates="identity",
        foreign_keys="UserAuditLog.identity_id",
    )

    def __repr__(self) -> str:
        return f"<Identity id={self.identity_id} type={self.principal_type!r}>"