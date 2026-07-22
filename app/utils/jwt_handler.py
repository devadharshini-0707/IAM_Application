"""JWT token creation and validation utilities."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.config.settings import get_settings


class JWTHandler:
    """Handles JWT access token generation and decoding."""

    def __init__(self) -> None:
        self._settings = get_settings()

    def create_access_token(
        self,
        *,
        user_id: str,
        organization_id: str,
    ) -> str:
        """Create JWT access token."""

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self._settings.access_token_expire_minutes
        )

        payload: dict[str, Any] = {
            "sub": user_id,
            "organization_id": organization_id,
            "exp": expire,
        }

        return jwt.encode(
            payload,
            self._settings.secret_key,
            algorithm=self._settings.jwt_algorithm,
        )

    def decode_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        """Decode and validate JWT token."""

        try:
            return jwt.decode(
                token,
                self._settings.secret_key,
                algorithms=[self._settings.jwt_algorithm],
            )

        except JWTError as exc:
            raise ValueError("Invalid token") from exc