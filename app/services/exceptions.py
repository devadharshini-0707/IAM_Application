"""Domain-level exceptions raised by the service layer.

Repositories raise nothing beyond what SQLAlchemy itself raises -- they
are pure data access, with no opinion on what counts as an error.
Business-rule violations ("that organization doesn't exist", "that slug
is already taken", "that status transition isn't valid") are judgment
calls, and per this project's Clean Architecture split that judgment
belongs to the service layer. Giving those violations their own
exception hierarchy here keeps callers (routes, scripts, tests) able to
handle them by intent instead of pattern-matching on ``None`` returns or
catching ``sqlalchemy.exc`` types that describe a storage failure, not a
business one.
"""

from __future__ import annotations


class ServiceError(Exception):
    """Base class for every exception raised by the service layer."""


class NotFoundError(ServiceError):
    """Raised when a requested entity does not exist."""


class ConflictError(ServiceError):
    """Raised when an operation would violate a uniqueness constraint or
    would leave the data in a self-contradictory state (e.g. deleting an
    organization that still has children)."""


class ValidationError(ServiceError):
    """Raised when caller-supplied data fails a business rule that isn't
    already enforced by the database schema (e.g. an unrecognized
    principal type)."""
