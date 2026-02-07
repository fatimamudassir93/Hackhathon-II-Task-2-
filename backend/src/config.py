from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost/dbname")

    # JWT settings
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")

    # Token expiration (24 hours default)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # Rate limiting
    RATE_LIMIT_DEFAULT: str = os.getenv("RATE_LIMIT_DEFAULT", "5/minute")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()