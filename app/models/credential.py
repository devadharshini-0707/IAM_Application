"""CREDENTIALS -- a user's authentication secret and rotation metadata,
isolated from USERS for security segregation.
"""

from __future__ import annotations

import datetime as dt
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.password_history import PasswordHistory
    from app.models.user import User


class Credential(Base):
    """A single authentication credential (password, API key, etc.) owned by a user.

    Maps to the ``CREDENTIALS`` table. Carries no ``updated_at`` column per
    the architecture PDF -- rotation is tracked via ``last_rotated_at``
    instead of a generic update timestamp.
    """

    __tablename__ = "credentials"

    credential_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    credential_type: Mapped[str] = mapped_column(String(20), nullable=False)
    hash: Mapped[str] = mapped_column(String(255), nullable=False)
    algorithm: Mapped[str] = mapped_column(String(30), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_rotated_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="credentials")
    password_history: Mapped[list["PasswordHistory"]] = relationship(
        "PasswordHistory", back_populates="credential"
    )

    def __repr__(self) -> str:
        return f"<Credential id={self.credential_id} type={self.credential_type!r}>"