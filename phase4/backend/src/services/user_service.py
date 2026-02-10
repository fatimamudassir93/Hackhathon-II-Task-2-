from sqlmodel import select, Session
from ..models.user import User, UserCreate
from ..utils.password import hash_password, validate_password_strength, verify_password
from ..utils.jwt import create_access_token
from datetime import timedelta
from typing import Optional
from uuid import uuid4
import uuid

class UserService:
    """Service class for user-related operations"""

    @staticmethod
    async def create_user(user_data: UserCreate, db_session) -> Optional[User]:
        """
        Create a new user
        Args:
            user_data: User creation data
            db_session: Database session
        Returns:
            Created user or None if creation failed
        """
        # Validate password strength
        is_valid, error_msg = validate_password_strength(user_data.password)
        if not is_valid:
            raise ValueError(error_msg)

        # Check if user with this email already exists
        existing_user = await db_session.exec(
            select(User).where(User.email == user_data.email)
        )
        existing_user = existing_user.first()

        if existing_user:
            raise ValueError("Email already registered")

        # Hash the password
        hashed_password = hash_password(user_data.password)

        # Create new user
        db_user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password
        )

        # Add to database
        db_session.add(db_user)
        await db_session.commit()
        await db_session.refresh(db_user)

        return db_user

    @staticmethod
    async def authenticate_user(email: str, password: str, db_session) -> Optional[User]:
        """
        Authenticate a user by email and password
        Args:
            email: User's email
            password: User's plain text password
            db_session: Database session
        Returns:
            User object if authentication successful, None otherwise
        """
        # Get user from database
        result = await db_session.exec(select(User).where(User.email == email))
        user = result.first()

        if not user:
            return None

        # Verify password
        if not user.hashed_password or not password:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    async def create_access_token_for_user(user: User) -> str:
        """
        Create an access token for a user
        Args:
            user: User object
        Returns:
            JWT access token
        """
        data = {"sub": user.id}
        token = create_access_token(data=data, expires_delta=timedelta(hours=24))  # 24 hour expiration
        return token