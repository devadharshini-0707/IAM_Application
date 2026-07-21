"""USER_AUDIT_LOGS -- immutable record of every significant action taken by
any identity, human or machine.
"""

from __future__ import annotations

import datetime as dt
import uuid
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.identity import Identity
    from app.models.organization import Organization


class UserAuditLog(Base):
    """A single immutable audit event attributed to an identity.

    Maps to the ``USER_AUDIT_LOGS`` table. The Python attribute
    ``event_metadata`` maps to the ``metadata`` column, since ``metadata``
    is a reserved name on SQLAlchemy's declarative base. ``target_resource_id``
    is a plain UUID with no foreign key constraint, since the PDF documents
    it as a polymorphic reference that may point at any resource table.
    """

    __tablename__ = "user_audit_logs"

    audit_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    identity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("identities.identity_id"), nullable=False
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.organization_id"), nullable=False
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    event_metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(
        "metadata", JSONB, nullable=True
    )
    occurred_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    identity: Mapped["Identity"] = relationship(
        "Identity", back_populates="audit_logs", foreign_keys=[identity_id]
    )
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="audit_logs", foreign_keys=[organization_id]
    )

    def __repr__(self) -> str:
        return f"<UserAuditLog id={self.audit_event_id} event_type={self.event_type!r}>"