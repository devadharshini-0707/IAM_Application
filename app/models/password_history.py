"""PASSWORD_HISTORY -- previous password hashes for a credential, enforcing
password-reuse prevention.
"""

from __future__ import annotations

import datetime as dt
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.credential import Credential


class PasswordHistory(Base):
    """A previously used password hash for a given credential.

    Maps to the ``PASSWORD_HISTORY`` table. No ``updated_at`` per the
    architecture PDF -- history rows are immutable once written.
    """

    __tablename__ = "password_history"

    history_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    credential_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("credentials.credential_id"), nullable=False
    )
    hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    credential: Mapped["Credential"] = relationship(
        "Credential", back_populates="password_history"
    )

    def __repr__(self) -> str:
        return f"<PasswordHistory id={self.history_id} credential_id={self.credential_id}>"