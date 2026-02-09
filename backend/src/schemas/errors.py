from pydantic import BaseModel
from typing import Optional, Dict, Any

class ErrorDetail(BaseModel):
    """Detailed error information"""
    type: str
    message: str
    code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: ErrorDetail

class ValidationErrorResponse(ErrorResponse):
    """Validation error response model"""
    error: ErrorDetail
    validation_errors: Optional[list] = None