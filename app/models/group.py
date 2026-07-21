"""GROUPS -- a collection of users within an organization for bulk access
management and organizational structuring.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user_group import UserGroup


class Group(Base, TimestampMixin):
    """A collection of users, optionally nested under a parent group.

    Maps to the ``GROUPS`` table. ``group_code`` is unique per
    organization; ``parent_group_id`` self-references for nested
    hierarchies, mirroring the ``Organization`` self-reference pattern.
    """

    __tablename__ = "groups"
    __table_args__ = (
        UniqueConstraint("organization_id", "group_code", name="uq_groups_org_code"),
    )

    group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.organization_id"), nullable=False
    )
    parent_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.group_id"), nullable=True
    )
    group_name: Mapped[str] = mapped_column(String(150), nullable=False)
    group_code: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="groups", foreign_keys=[organization_id]
    )
    parent: Mapped[Optional["Group"]] = relationship(
        "Group", remote_side="Group.group_id", back_populates="children"
    )
    children: Mapped[list["Group"]] = relationship("Group", back_populates="parent")
    user_groups: Mapped[list["UserGroup"]] = relationship(
        "UserGroup", back_populates="group"
    )

    def __repr__(self) -> str:
        return f"<Group id={self.group_id} code={self.group_code!r}>"