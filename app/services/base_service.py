"""Shared base class for every service in this package.

Centralizes transaction-boundary management -- commit on success, roll
back on any exception -- so that concrete services only need to describe
*what* a use case does with its repositories, not how the surrounding
unit of work is opened and closed. Repositories only ``flush`` (see
``app.repositories.base_repository``); this class is where those flushed
changes actually become durable, which keeps the decision of "does this
use case succeed or fail as a whole" in the service layer rather than
scattered across repositories or pushed up to the route layer.

This class belongs to the Clean Architecture "use cases" layer. It
depends on SQLAlchemy's ``Session`` only to call ``commit()`` /
``rollback()`` at the boundary of a use case -- concrete services never
issue queries against it directly; all actual data access happens
through the repositories they're constructed with.
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.base_repository import BaseRepository
from app.services.exceptions import ConflictError


class BaseService:
    """Provides the transaction boundary shared by every concrete service.

    Concrete services accept the repositories they need plus the same
    ``Session`` instance those repositories were constructed with, then
    wrap each use case that mutates state in ``self._transaction()``.
    Read-only use cases (a plain lookup or list) can skip it entirely,
    since they issue no writes to commit.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    @contextmanager
    def _transaction(self) -> Generator[None, None, None]:
        """Commit the session if the wrapped block succeeds; otherwise roll
        it back and re-raise, so a use case spanning several repository
        calls either lands completely or not at all.
        """
        try:
            yield
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise

    def _delete_with_integrity_guard(
        self,
        repository: BaseRepository[Any, Any],
        entity: Any,
        *,
        conflict_message: str,
    ) -> None:
        """Delete ``entity`` via ``repository``, translating a foreign-key
        constraint violation into a ``ConflictError`` with a caller-supplied,
        human-readable message instead of letting a raw ``IntegrityError``
        leak up to callers that shouldn't need to know the storage layer
        raised it.
        """
        try:
            repository.delete(entity)
        except IntegrityError as exc:
            raise ConflictError(conflict_message) from exc
