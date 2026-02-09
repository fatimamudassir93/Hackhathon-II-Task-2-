from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from ..schemas.errors import ErrorResponse, ValidationErrorResponse, ErrorDetail
from slowapi.errors import RateLimitExceeded
from typing import Dict, Any

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions
    """
    error_detail = ErrorDetail(
        type="http_error",
        message=exc.detail if hasattr(exc, 'detail') else "An HTTP error occurred",
        code=str(exc.status_code)
    )

    error_response = ErrorResponse(error=error_detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle request validation exceptions
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error['loc'],
            "msg": error['msg'],
            "type": error['type']
        })

    error_detail = ErrorDetail(
        type="validation_error",
        message="Request validation failed",
        code="400"
    )

    error_response = ValidationErrorResponse(
        error=error_detail,
        validation_errors=errors
    )

    return JSONResponse(
        status_code=400,
        content=error_response.dict()
    )

async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    """
    Handle rate limit exceeded exceptions
    """
    error_detail = ErrorDetail(
        type="rate_limit_error",
        message="Rate limit exceeded",
        code="429",
        details={
            "retry_after": getattr(exc, 'retry_after', None)
        }
    )

    error_response = ErrorResponse(error=error_detail)
    return JSONResponse(
        status_code=429,
        content=error_response.dict()
    )

async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions
    """
    error_detail = ErrorDetail(
        type="internal_error",
        message="An internal server error occurred",
        code="500"
    )

    error_response = ErrorResponse(error=error_detail)
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )