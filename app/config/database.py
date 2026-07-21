"""Database engine and session management for the IAM application.

This module is intentionally decoupled from Flask itself. Repositories and
services receive a SQLAlchemy ``Session`` through constructor injection
rather than reaching into a framework-global object, which keeps the data
layer testable in isolation and keeps Flask an implementation detail of the
web layer rather than a dependency of the domain layer.
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config.settings import get_settings

settings = get_settings()

engine: Engine = create_engine(
    settings.database_url,
    echo=settings.sqlalchemy_echo,
    pool_pre_ping=True,
    future=True,
)

SessionFactory: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)


class Base(DeclarativeBase):
    """Declarative base class shared by every ORM model in the application.

    Every model in ``app.models`` must inherit from this class so that
    Alembic's autogenerate can discover the full set of mapped tables from
    a single metadata object.
    """


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Yield a transactional SQLAlchemy session.

    Intended for use by the application's dependency-injection wiring (e.g.
    a Flask request hook or a service factory), not called directly by
    repositories or services. Commits on clean exit, rolls back on
    exception, and always closes the session.
    """
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()                 