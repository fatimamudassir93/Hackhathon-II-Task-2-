import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import tasks
from chatbot.routes import chat
from src.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    rate_limit_exception_handler,
    general_exception_handler
)
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from src.middleware.rate_limit import setup_rate_limiter

# Create FastAPI app
app = FastAPI(title="Todo App API", version="1.0.0")

# Configure CORS for production deployment
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url] if frontend_url else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup rate limiter
setup_rate_limiter(app)

# Include routers (auth routes removed - Better Auth handles authentication)
app.include_router(tasks.router)
app.include_router(chat.router)

# Register exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo App API"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Todo App API",
        "version": "1.0.0",
        "llm_provider": os.getenv("LLM_PROVIDER", "not configured")
    }

# Create database tables on startup
@app.on_event("startup")
async def on_startup():
    from src.models.task import Task
    from chatbot.models.conversation import ConversationMessage
    from src.models.tag import Tag, TaskTag
    from src.models.reminder import Reminder
    from src.database.database import sync_engine

    # Create tables (User table is managed by Better Auth)
    # Only create application-specific tables
    from sqlmodel import SQLModel

    # Get metadata for only the tables we want to create
    tables_to_create = [
        Task.__table__,
        ConversationMessage.__table__,
        Tag.__table__,
        TaskTag.__table__,
        Reminder.__table__
    ]

    for table in tables_to_create:
        table.create(bind=sync_engine, checkfirst=True)