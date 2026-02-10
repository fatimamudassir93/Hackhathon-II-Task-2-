from pydantic import BaseModel
from typing import Optional, Dict, Any

class BaseResponse(BaseModel):
    """Base response model for all API responses"""
    success: bool
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    error: Dict[str, Any]

class TokenResponse(BaseModel):
    """Response model for JWT token"""
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    """Response model for user data"""
    id: str
    email: str
    name: str
    created_at: str
    updated_at: str