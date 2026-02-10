from fastapi import FastAPI
from src.routes import auth, tasks
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

# Setup rate limiter
setup_rate_limiter(app)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

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
    return {"status": "healthy", "service": "Todo App API"}

# Create database tables on startup
@app.on_event("startup")
async def on_startup():
    from sqlmodel import create_engine
    from src.models.user import User
    from src.models.task import Task
    from src.database.database import sync_engine

    # Create tables
    User.metadata.create_all(bind=sync_engine)
    Task.metadata.create_all(bind=sync_engine)