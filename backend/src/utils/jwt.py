from datetime import datetime, timedelta
from typing import Optional
import jwt
from ..config import settings

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token with the given data
    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta
    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})

    encoded_jwt = jwt.encode(to_encode, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token
    Args:
        token: JWT token to verify
    Returns:
        Decoded token data if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.JWTError:
        # Invalid token
        return None

def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from a JWT token
    Args:
        token: JWT token to extract user ID from
    Returns:
        User ID if found and valid, None otherwise
    """
    payload = verify_token(token)
    if payload:
        return payload.get("sub")  # subject typically holds the user ID
    return None