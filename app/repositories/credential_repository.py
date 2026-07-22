from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.credential import Credential
from app.repositories.base_repository import BaseRepository


class CredentialRepository(BaseRepository[Credential, uuid.UUID]):
    """Repository for user credentials."""

    model = Credential

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_active_password_credential(
        self,
        user_id: uuid.UUID,
    ) -> Optional[Credential]:
        """Return active password credential for user."""

        stmt = select(Credential).where(
            Credential.user_id == user_id,
            Credential.credential_type == "password",
            Credential.is_active.is_(True),
        )

        return self._session.scalars(stmt).first()
   