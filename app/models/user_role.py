"""USER_ROLES -- many-to-many join assigning roles to users (role mapping)."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.user import User


class UserRole(Base):
    """A single role assignment granted to a user.

    Maps to the ``USER_ROLES`` table. No ``created_at``/``updated_at`` per
    the architecture PDF -- ``assigned_at`` records the grant. ``assigned_by``
    is a plain tracking column, not a full relationship, since it is
    administrative metadata rather than a structural link.
    """

    __tablename__ = "user_roles"
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_roles_user_role"),
    )

    user_role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.role_id"), nullable=False
    )
    assigned_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True
    )
    assigned_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expires_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="user_roles", foreign_keys=[user_id]
    )
    role: Mapped["Role"] = relationship(
        "Role", back_populates="user_roles", foreign_keys=[role_id]
    )

    def __repr__(self) -> str:
        return f"<UserRole id={self.user_role_id} user_id={self.user_id} role_id={self.role_id}>"