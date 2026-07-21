"""AUTHENTICATION_POLICIES -- organization-level rules for password
strength, MFA enforcement, and session duration.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.organization import Organization


class AuthenticationPolicy(Base, TimestampMixin):
    """The single active authentication policy for one organization.

    Maps to the ``AUTHENTICATION_POLICIES`` table. The unique FK on
    ``organization_id`` enforces the PDF's documented 1:1 relationship
    between ``ORGANIZATIONS`` and ``AUTHENTICATION_POLICIES``.
    """

    __tablename__ = "authentication_policies"

    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.organization_id"),
        nullable=False,
        unique=True,
    )
    min_password_length: Mapped[int] = mapped_column(Integer, nullable=False)
    mfa_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    max_session_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="authentication_policy"
    )

    def __repr__(self) -> str:
        return f"<AuthenticationPolicy id={self.policy_id} org_id={self.organization_id}>"