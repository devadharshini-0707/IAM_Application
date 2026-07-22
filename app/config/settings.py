"""Typed application settings loaded from environment variables.

Uses ``pydantic-settings`` rather than raw ``os.environ`` lookups so that
every config value is validated and typed at startup -- a missing or
malformed ``DATABASE_URL``, for example, fails immediately with a clear
error instead of surfacing later as a cryptic SQLAlchemy exception.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration, sourced from environment variables / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: str = "development"
    secret_key: str
    database_url: str
    log_level: str = "INFO"
    sqlalchemy_echo: bool = False


@lru_cache
def get_settings() -> Settings:
    """Return a cached, process-wide ``Settings`` instance.

    A cached factory function -- rather than a module-level singleton built
    at import time -- keeps settings access explicit and easy to override in
    tests via ``get_settings.cache_clear()`` plus environment patching,
    instead of relying on import-order side effects.
    """
    return Settings()