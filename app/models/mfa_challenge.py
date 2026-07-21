"""MFA_CHALLENGES -- individual verification attempts issued against a
registered MFA factor during login.
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
    from app.models.mfa_factor import MfaFactor


class MfaChallenge(Base):
    """A single MFA verification attempt against an enrolled factor.

    Maps to the ``MFA_CHALLENGES`` table. No ``updated_at`` per the
    architecture PDF -- ``status`` transitions are tracked in place.
    """

    __tablename__ = "mfa_challenges"

    challenge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    mfa_factor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("mfa_factors.mfa_factor_id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    challenge_code_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    verified_at: Mapped[Optional[dt.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    mfa_factor: Mapped["MfaFactor"] = relationship(
        "MfaFactor", back_populates="mfa_challenges"
    )

    def __repr__(self) -> str:
        return f"<MfaChallenge id={self.challenge_id} status={self.status!r}>"