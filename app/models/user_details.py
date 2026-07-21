"""USER_DETAILS -- extended personal, contact, and address information for
a user, kept separate from USERS so login-critical data stays lean while
descriptive profile data can grow and be governed independently.
"""

from __future__ import annotations

import datetime as dt
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class UserDetails(Base, TimestampMixin):
    """Extended profile information for a user.

    Maps to the ``USER_DETAILS`` table (renamed in this revision from
    USER_PROFILES). One-to-one with ``USERS`` via a unique ``user_id``
    foreign key.
    """

    __tablename__ = "user_details"

    user_details_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False,
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    preferred_display_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    date_of_birth: Mapped[Optional[dt.date]] = mapped_column(Date, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    alternate_phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False)
    locale: Mapped[str] = mapped_column(String(10), nullable=False)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="details",
    )

    def __repr__(self) -> str:
        return f"<UserDetails id={self.user_details_id} user_id={self.user_id}>"