from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from ..database.session import get_db_session
from ..schemas.user import UserRegistrationRequest, UserRegistrationResponse, UserLoginRequest, UserLoginResponse
from ..services.user_service import UserService
from ..models.user import User, UserCreate
from ..utils.validation import validate_email_format, validate_password_strength, validate_user_name
from ..schemas.responses import TokenResponse, UserResponse
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/api")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/signup", response_model=UserRegistrationResponse)
@limiter.limit("5/minute")  # Rate limit to 5 requests per minute
async def register_user(
    request: Request,
    user_data: UserRegistrationRequest,
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Register a new user
    """
    try:
        # Validate email format
        is_valid_email, email_error = validate_email_format(user_data.email)
        if not is_valid_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=email_error
            )

        # Validate password strength
        is_valid_password, password_error = validate_password_strength(user_data.password)
        if not is_valid_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=password_error
            )

        # Validate user name
        is_valid_name, name_error = validate_user_name(user_data.name)
        if not is_valid_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=name_error
            )

        # Create user through service
        user_create_data = UserCreate(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name
        )

        user = await UserService.create_user(user_create_data, db_session)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Create access token
        token_str = await UserService.create_access_token_for_user(user)
        token_response = TokenResponse(access_token=token_str, token_type="bearer")

        # Format user response
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at.isoformat() if user.created_at else "",
            updated_at=user.updated_at.isoformat() if user.updated_at else ""
        )

        return UserRegistrationResponse(user=user_response, token=token_response)

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )


@router.post("/signin", response_model=UserLoginResponse)
@limiter.limit("5/minute")  # Rate limit to 5 requests per minute
async def login_user(
    request: Request,
    login_data: UserLoginRequest,
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Authenticate a user and return JWT token
    """
    try:
        # Validate email format
        is_valid_email, email_error = validate_email_format(login_data.email)
        if not is_valid_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=email_error
            )

        # Authenticate user
        user = await UserService.authenticate_user(
            login_data.email,
            login_data.password,
            db_session
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Create access token
        token_str = await UserService.create_access_token_for_user(user)
        token_response = TokenResponse(access_token=token_str, token_type="bearer")

        # Format user response
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at.isoformat() if user.created_at else "",
            updated_at=user.updated_at.isoformat() if user.updated_at else ""
        )

        return UserLoginResponse(user=user_response, token=token_response)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )