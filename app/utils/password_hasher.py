"""Password hashing and verification utilities."""

import bcrypt


class PasswordHasher:
    """Handles password hashing and verification."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Generate a secure password hash."""

        password_bytes = password.encode("utf-8")

        hashed = bcrypt.hashpw(
            password_bytes,
            bcrypt.gensalt(),
        )

        return hashed.decode("utf-8")
        
    @staticmethod
    def verify_password(
    plain_password: str, 
    password_hash: str,
    ) -> bool:
        """Verify plain password against stored hash."""

        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )