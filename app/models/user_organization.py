"""USER_ORGANIZATIONS -- many-to-many join resolving which organizations a
user belongs to, since a single enterprise user can legitimately hold
membership in more than one tenant.

Deliberately has no TimestampMixin: the PDF gives this table only
``joined_at``, not ``created_at``/``updated_at`` -- membership rows are
recorded once at join time, not expected to be updated in place.
"""

from __future__ import annotations

import datetime as dt
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user import User


class UserOrganization(Base):
    """A user's membership in a single organization (tenant).

    Maps to the ``USER_ORGANIZATIONS`` table. ``ou_id`` is carried as a
    plain nullable UUID with no foreign key, per the PDF's note that it is
    reserved for a future Org-Structure module not yet modeled.
    """

    __tablename__ = "user_organizations"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "organization_id", name="uq_user_organizations_user_org"
        ),
    )

    user_organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.organization_id"),
        nullable=False,
    )
    ou_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    joined_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="organization_memberships",
        foreign_keys=[user_id],
    )
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="user_memberships",
        foreign_keys=[organization_id],
    )

    def __repr__(self) -> str:
        return (
            f"<UserOrganization user_id={self.user_id} "
            f"organization_id={self.organization_id}>"
        )