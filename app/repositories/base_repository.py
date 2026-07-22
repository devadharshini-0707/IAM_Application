"""Generic base repository shared by every concrete repository in this
package.

Centralizes the CRUD mechanics that are identical across all repositories
(session-scoped add/flush, primary-key lookup, delete, unfiltered listing)
so that concrete repositories only implement the query methods specific
to their own model. This class belongs to the Clean Architecture
"interface adapters" layer -- it is the only place allowed to depend on
SQLAlchemy so that the service/domain layer above it never has to.

Transaction boundaries (commit/rollback) are intentionally *not* handled
here: the session is injected by the caller, which also owns when the
unit of work is committed or rolled back (see ``app.config.database``'s
``get_db`` / ``get_db_session``). Repository methods only ``flush``,
which is enough to send pending SQL to the database and populate
server-generated values (primary keys, timestamps) without ending the
transaction early.
"""

from __future__ import annotations

from typing import Generic, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.database import Base

ModelT = TypeVar("ModelT", bound=Base)
IdT = TypeVar("IdT")


class BaseRepository(Generic[ModelT, IdT]):
    """Session-scoped CRUD primitives shared by every repository.

    Generic over both the ORM model (``ModelT``) and its primary-key type
    (``IdT``), e.g. ``BaseRepository[Organization, uuid.UUID]``. Typing the
    primary key explicitly -- rather than accepting ``object`` -- lets each
    concrete repository's ``get_by_id`` stay a proper, non-widening
    override instead of silently accepting any type. Concrete subclasses
    also set the ``model`` class attribute to the ORM model they wrap, so
    the CRUD methods below stay fully typed without repeating themselves
    in every subclass.
    """

    model: type[ModelT]

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: ModelT) -> ModelT:
        """Stage a new entity for insertion and flush it to the database.

        Flushing (rather than committing) makes server-generated defaults
        -- primary keys, ``created_at``/``updated_at`` -- available on the
        returned instance while leaving the transaction open for the
        caller to commit or extend.
        """
        self._session.add(entity)
        self._session.flush()
        return entity

    def update(self, entity: ModelT) -> ModelT:
        """Persist changes made to an already-tracked entity.

        ``Session.add`` is a no-op for an instance the session already
        tracks, so this simply flushes pending attribute changes; it is
        provided as a distinct, explicitly-named method so call sites read
        as "update" rather than reusing ``add`` for a different intent.
        """
        self._session.add(entity)
        self._session.flush()
        return entity

    def delete(self, entity: ModelT) -> None:
        """Mark an entity for deletion and flush the change."""
        self._session.delete(entity)
        self._session.flush()

    def get_by_id(self, entity_id: IdT) -> Optional[ModelT]:
        """Look up a single row by its primary key, regardless of the
        primary key column's name on the concrete model."""
        return self._session.get(self.model, entity_id)

    def list_all(
        self, *, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> list[ModelT]:
        """Return every row for this repository's model, optionally paged."""
        stmt = select(self.model)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        return list(self._session.scalars(stmt))
