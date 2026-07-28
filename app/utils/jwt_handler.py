from datetime import datetime, timedelta, UTC

import jwt

from app.config.settings import get_settings

settings = get_settings()


class JWTHandler:
    @staticmethod
    def create_access_token(user_id: str) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.now(UTC)
            + timedelta(minutes=settings.access_token_expire_minutes),
        }

        return jwt.encode(
            payload,
            settings.secret_key,
            algorithm=settings.jwt_algorithm,
        )

    @staticmethod
    def decode_token(token: str):
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )