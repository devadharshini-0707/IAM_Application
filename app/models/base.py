"""Shared model mixins for the IAM application's ORM layer.

Centralizing cross-cutting columns here keeps every concrete model focused
solely on the columns and relationships that make it unique.
"""

from __future__ import annotations

import datetime as dt

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TimestampMixin:
    """Adds ``created_at`` / ``updated_at`` columns, present on every table
    in the architecture PDF.

    ``server_default=func.now()`` sets the value in the database itself,
    not in Python, so the timestamp is correct even for rows inserted
    outside the application and stays consistent under concurrent writes.
    """

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )