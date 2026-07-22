"""Use-case layer for the ``UserDetails`` aggregate -- extended personal,
contact, and address information for a user.

Enforces the business rules ``UserDetailsRepository`` deliberately leaves
out (user existence, the one-to-one link between a ``User`` and its
``UserDetails`` row) and owns the transaction boundary around each use
case. Depends only on ``UserDetailsRepository`` and ``UserRepository``,
never on ``sqlalchemy`` or a raw ``Session`` query.
"""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Final, Optional, TypeVar, Union

from sqlalchemy.orm import Session

from app.models.user_details import UserDetails
from app.repositories.user_details_repository import UserDetailsRepository
from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService
from app.services.exceptions import ConflictError, NotFoundError

_T = TypeVar("_T")


class _UnsetType:
    """Sentinel type distinguishing "this field was not supplied" from an
    explicit ``None``, since most ``UserDetails`` columns are themselves
    nullable -- a real update needs to be able to *clear* a field, not
    just leave every unspecified parameter indistinguishable from that.
    """

    def __repr__(self) -> str:
        return "UNSET"


#: Sentinel default for the optional keyword arguments of
#: ``update_user_details``. See ``_UnsetType``.
UNSET: Final = _UnsetType()

#: A value that is either a real ``_T`` (including ``None``, for nullable
#: columns) or the ``UNSET`` sentinel meaning "leave this field alone".
Maybe = Union[_T, _UnsetType]


class UserDetailsService(BaseService):
    """Use cases for creating, looking up, and managing extended user
    profile information."""

    def __init__(
        self,
        session: Session,
        user_details_repository: UserDetailsRepository,
        user_repository: UserRepository,
    ) -> None:
        super().__init__(session)
        self._user_details = user_details_repository
        self._users = user_repository

    def create_user_details(
        self,
        *,
        user_id: uuid.UUID,
        first_name: str,
        last_name: str,
        timezone: str,
        locale: str,
        middle_name: Optional[str] = None,
        preferred_display_name: Optional[str] = None,
        gender: Optional[str] = None,
        date_of_birth: Optional[dt.date] = None,
        phone_number: Optional[str] = None,
        alternate_phone: Optional[str] = None,
        avatar_url: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        postal_code: Optional[str] = None,
    ) -> UserDetails:
        """Create the extended profile row for a user.

        Raises:
            NotFoundError: no user exists with that id.
            ConflictError: the user already has a profile row.
        """
        with self._transaction():
            if self._users.get_by_id(user_id) is None:
                raise NotFoundError(f"User {user_id} does not exist.")
            if self._user_details.exists_by_user_id(user_id):
                raise ConflictError(f"User {user_id} already has a profile.")
            details = UserDetails(
                user_id=user_id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                preferred_display_name=preferred_display_name,
                gender=gender,
                date_of_birth=date_of_birth,
                phone_number=phone_number,
                alternate_phone=alternate_phone,
                avatar_url=avatar_url,
                address=address,
                city=city,
                state=state,
                country=country,
                postal_code=postal_code,
                timezone=timezone,
                locale=locale,
            )
            return self._user_details.add(details)

    def get_user_details(self, user_details_id: uuid.UUID) -> UserDetails:
        """Return the profile row with the given primary key.

        Raises:
            NotFoundError: no profile exists with that id.
        """
        details = self._user_details.get_by_id(user_details_id)
        if details is None:
            raise NotFoundError(f"User profile {user_details_id} does not exist.")
        return details

    def get_user_details_by_user(self, user_id: uuid.UUID) -> UserDetails:
        """Return the profile belonging to the given user.

        Raises:
            NotFoundError: the user has no profile row.
        """
        details = self._user_details.get_by_user_id(user_id)
        if details is None:
            raise NotFoundError(f"User {user_id} has no profile.")
        return details

    def update_user_details(
        self,
        user_id: uuid.UUID,
        *,
        first_name: Maybe[str] = UNSET,
        middle_name: Maybe[Optional[str]] = UNSET,
        last_name: Maybe[str] = UNSET,
        preferred_display_name: Maybe[Optional[str]] = UNSET,
        gender: Maybe[Optional[str]] = UNSET,
        date_of_birth: Maybe[Optional[dt.date]] = UNSET,
        phone_number: Maybe[Optional[str]] = UNSET,
        alternate_phone: Maybe[Optional[str]] = UNSET,
        avatar_url: Maybe[Optional[str]] = UNSET,
        address: Maybe[Optional[str]] = UNSET,
        city: Maybe[Optional[str]] = UNSET,
        state: Maybe[Optional[str]] = UNSET,
        country: Maybe[Optional[str]] = UNSET,
        postal_code: Maybe[Optional[str]] = UNSET,
        timezone: Maybe[str] = UNSET,
        locale: Maybe[str] = UNSET,
    ) -> UserDetails:
        """Partially update a user's profile.

        Every field defaults to the ``UNSET`` sentinel and is left
        untouched unless explicitly passed -- including with a value of
        ``None``, which clears a nullable field rather than being
        mistaken for "not supplied".

        Raises:
            NotFoundError: the user has no profile row.
        """
        with self._transaction():
            details = self.get_user_details_by_user(user_id)
            updates = {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "preferred_display_name": preferred_display_name,
                "gender": gender,
                "date_of_birth": date_of_birth,
                "phone_number": phone_number,
                "alternate_phone": alternate_phone,
                "avatar_url": avatar_url,
                "address": address,
                "city": city,
                "state": state,
                "country": country,
                "postal_code": postal_code,
                "timezone": timezone,
                "locale": locale,
            }
            for field_name, value in updates.items():
                if value is not UNSET:
                    setattr(details, field_name, value)
            return self._user_details.update(details)

    def delete_user_details(self, user_id: uuid.UUID) -> None:
        """Delete a user's profile row.

        Raises:
            NotFoundError: the user has no profile row.
        """
        with self._transaction():
            details = self.get_user_details_by_user(user_id)
            self._user_details.delete(details)
