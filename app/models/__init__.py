"""ORM model package.

Every model must be imported here so that ``Base.metadata`` is fully
populated before Alembic's autogenerate, or any direct
``Base.metadata.create_all`` call, runs.
"""

from app.models.authentication_policy import AuthenticationPolicy
from app.models.credential import Credential
from app.models.group import Group
from app.models.identity import Identity
from app.models.mfa_challenge import MfaChallenge
from app.models.mfa_factor import MfaFactor
from app.models.organization import Organization
from app.models.password_history import PasswordHistory
from app.models.role import Role
from app.models.role_swap import RoleSwap
from app.models.user import User
from app.models.user_audit_log import UserAuditLog
from app.models.user_details import UserDetails
from app.models.user_group import UserGroup
from app.models.user_organization import UserOrganization
from app.models.user_role import UserRole

__all__ = [
    "AuthenticationPolicy",
    "Credential",
    "Group",
    "Identity",
    "MfaChallenge",
    "MfaFactor",
    "Organization",
    "PasswordHistory",
    "Role",
    "RoleSwap",
    "User",
    "UserAuditLog",
    "UserDetails",
    "UserGroup",
    "UserOrganization",
    "UserRole",
]