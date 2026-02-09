import bcrypt
from typing import Union

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    Args:
        password: Plain text password
    Returns:
        Hashed password as string
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password to compare against
    Returns:
        True if password matches, False otherwise
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength according to requirements
    Args:
        password: Password to validate
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    if not (has_upper and has_lower and has_digit):
        return False, "Password must contain uppercase, lowercase, and numeric characters"

    return True, ""