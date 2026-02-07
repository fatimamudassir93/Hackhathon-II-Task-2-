import re
from typing import Tuple

def validate_email_format(email: str) -> Tuple[bool, str]:
    """
    Validate email format
    Args:
        email: Email address to validate
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Regular expression for email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_regex, email):
        return False, "Invalid email format"

    return True, ""

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength
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
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    if not (has_upper and has_lower and has_digit):
        return False, "Password must contain uppercase, lowercase, and numeric characters"

    return True, ""

def validate_user_name(name: str) -> Tuple[bool, str]:
    """
    Validate user name
    Args:
        name: Name to validate
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or len(name.strip()) == 0:
        return False, "Name cannot be empty"

    if len(name) > 255:
        return False, "Name must be 255 characters or less"

    return True, ""