from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
from ..utils.jwt import verify_token, get_user_id_from_token

security = HTTPBearer()

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to extract current user ID from JWT token
    Args:
        credentials: HTTP Authorization credentials
    Returns:
        User ID from token
    Raises:
        HTTPException: If token is invalid, expired, or user ID is missing
    """
    token = credentials.credentials

    # Verify the token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user ID from token
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id

def verify_user_id_match_path(path_user_id: str, current_user_id: str) -> bool:
    """
    Verify that the current user ID matches the user ID in the path
    Args:
        path_user_id: User ID from the request path
        current_user_id: User ID from the JWT token
    Returns:
        True if IDs match, raises HTTPException if they don't
    Raises:
        HTTPException: If user IDs don't match (403 Forbidden)
    """
    if current_user_id != path_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )

    return True