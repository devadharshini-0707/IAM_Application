"""MFA_FACTORS -- second-factor authentication methods enrolled by a user."""

from __future__ import annotations

import datetime as dt
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.mfa_challenge import MfaChallenge
    from app.models.user import User


class MfaFactor(Base):
    """A single enrolled MFA factor (authenticator app, SMS, etc.) for a user.

    Maps to the ``MFA_FACTORS`` table. No ``updated_at`` per the
    architecture PDF.
    """

    __tablename__ = "mfa_factors"

    mfa_factor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    factor_type: Mapped[str] = mapped_column(String(20), nullable=False)
    secret_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="mfa_factors")
    mfa_challenges: Mapped[list["MfaChallenge"]] = relationship(
        "MfaChallenge", back_populates="mfa_factor"
    )

    def __repr__(self) -> str:
        return f"<MfaFactor id={self.mfa_factor_id} type={self.factor_type!r}>"