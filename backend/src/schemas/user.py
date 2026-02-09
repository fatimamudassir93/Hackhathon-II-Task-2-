from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .responses import TokenResponse, UserResponse

class UserRegistrationRequest(BaseModel):
    """Request schema for user registration"""
    email: EmailStr
    password: str
    name: str

class UserRegistrationResponse(BaseModel):
    """Response schema for user registration"""
    user: UserResponse
    token: TokenResponse

class UserLoginRequest(BaseModel):
    """Request schema for user login"""
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    """Response schema for user login"""
    user: UserResponse
    token: TokenResponse