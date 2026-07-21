"""USER_GROUPS -- many-to-many join assigning users to groups (group mapping)."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.group import Group
    from app.models.user import User


class UserGroup(Base):
    """A single membership record linking a user to a group.

    Maps to the ``USER_GROUPS`` table. No ``created_at``/``updated_at`` per
    the architecture PDF -- ``joined_at`` records when membership began.
    ``added_by`` is a plain tracking column, not a full relationship.
    """

    __tablename__ = "user_groups"
    __table_args__ = (
        UniqueConstraint("user_id", "group_id", name="uq_user_groups_user_group"),
    )

    user_group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.group_id"), nullable=False
    )
    joined_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    added_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="user_groups", foreign_keys=[user_id]
    )
    group: Mapped["Group"] = relationship(
        "Group", back_populates="user_groups", foreign_keys=[group_id]
    )

    def __repr__(self) -> str:
        return f"<UserGroup id={self.user_group_id} user_id={self.user_id} group_id={self.group_id}>"