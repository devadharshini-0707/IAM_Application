"""ROLE_SWAPS -- a controlled role swap, reassigning a user from one
currently-held role to a different role in a single accountable action.
"""

from __future__ import annotations

import datetime as dt
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.user import User
    from app.models.user_role import UserRole


class RoleSwap(Base):
    """A single role-swap event, distinct from the routine grant/revoke
    history implied by USER_ROLES.

    Maps to the ``ROLE_SWAPS`` table. ``from_role_id``, ``to_role_id``, and
    ``user_role_id`` are unidirectional relationships (no back_populates),
    since ``Role``, ``User``, and ``UserRole`` do not need a reverse
    collection for this audit-style link. ``swapped_by`` is a plain
    tracking column.
    """

    __tablename__ = "role_swaps"

    role_swap_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    from_role_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.role_id"), nullable=True
    )
    to_role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.role_id"), nullable=False
    )
    user_role_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_roles.user_role_id"), nullable=True
    )
    swapped_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True
    )
    reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    swapped_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    from_role: Mapped[Optional["Role"]] = relationship(
        "Role", foreign_keys=[from_role_id]
    )
    to_role: Mapped["Role"] = relationship("Role", foreign_keys=[to_role_id])
    user_role: Mapped[Optional["UserRole"]] = relationship(
        "UserRole", foreign_keys=[user_role_id]
    )

    def __repr__(self) -> str:
        return f"<RoleSwap id={self.role_swap_id} user_id={self.user_id}>"