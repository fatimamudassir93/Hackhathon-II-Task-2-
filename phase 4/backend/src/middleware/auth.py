from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
from ..utils.jwt import verify_token
from ..models.user import User

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Dependency to get current user from JWT token
    Args:
        credentials: HTTP Authorization credentials
    Returns:
        User data dictionary from token
    Raises:
        HTTPException: If token is invalid or expired
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

    # Create a user-like object with just the ID
    user_data = {
        "id": user_id,
        "email": payload.get("email", ""),  # Email might not be in all tokens
        "name": payload.get("name", "")     # Name might not be in all tokens
    }

    return user_data

async def verify_user_owns_resource(current_user: Dict = Depends(get_current_user)) -> Dict:
    """
    Verify that the current user owns the requested resource
    Args:
        current_user: Current authenticated user
    Returns:
        Current user data
    """
    return current_user

def require_authenticated_user():
    """
    Dependency to require an authenticated user
    """
    return Depends(get_current_user)