# Todo App - FastAPI Backend

## Overview

This is the FastAPI backend for the Phase II Todo application. It provides RESTful API endpoints for task management with JWT-based authentication and user isolation.

## Technology Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Rate Limiting**: slowapi

## Prerequisites

- Python 3.10 or higher
- Neon PostgreSQL database (or compatible PostgreSQL instance)
- pip or poetry for dependency management

## Installation

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Configuration

1. **Create a `.env` file** in the `backend/` directory:
   ```bash
   cp .env.example .env
   ```

2. **Configure environment variables** in `.env`:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Shared secret for JWT signing/verification (must match frontend)

See `.env.example` for the complete list of required variables.

## Running the Server

### Development Mode

Run the FastAPI server with auto-reload:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Production Mode

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/signup` | Register a new user | No |
| POST | `/api/signin` | Authenticate user and get JWT token | No |

### Task Endpoints (Protected)

All task endpoints require a valid JWT token in the `Authorization: Bearer <token>` header.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for the user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get a specific task |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle task completion status |

## Authentication Flow

1. User signs up or signs in via the frontend (Better Auth)
2. Backend validates credentials and issues a JWT token
3. Frontend includes the JWT token in the `Authorization` header for all API requests
4. Backend validates the token and extracts the user ID
5. Backend verifies that the token's user ID matches the URL's user ID
6. Backend filters all data by the authenticated user's ID

## Security Features

- **JWT Authentication**: All protected endpoints require valid JWT tokens
- **User Isolation**: Users can only access their own tasks
- **Password Hashing**: Passwords are hashed using bcrypt before storage
- **Rate Limiting**: Authentication endpoints are rate-limited to prevent brute force attacks
- **Input Validation**: All inputs are validated using Pydantic models
- **Authorization Checks**: Cross-user access attempts return 403 Forbidden

## Project Structure

```
backend/
├── src/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database/
│   │   ├── database.py         # Database engine setup
│   │   └── session.py          # Database session management
│   ├── models/
│   │   ├── user.py             # User SQLModel
│   │   └── task.py             # Task SQLModel
│   ├── routes/
│   │   ├── auth.py             # Authentication endpoints
│   │   └── tasks.py            # Task CRUD endpoints
│   ├── services/
│   │   ├── user_service.py     # User business logic
│   │   └── task_service.py     # Task business logic
│   ├── schemas/
│   │   ├── user.py             # User request/response schemas
│   │   ├── responses.py        # Common response schemas
│   │   └── errors.py           # Error response schemas
│   ├── middleware/
│   │   ├── auth.py             # JWT authentication middleware
│   │   └── rate_limit.py       # Rate limiting setup
│   ├── dependencies/
│   │   └── auth.py             # Authentication dependencies
│   ├── utils/
│   │   ├── jwt.py              # JWT utilities
│   │   ├── password.py         # Password hashing utilities
│   │   └── validation.py       # Input validation utilities
│   └── exceptions/
│       └── handlers.py         # Exception handlers
├── .env                        # Environment variables (not in git)
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Error Responses

The API returns standardized error responses:

- **400 Bad Request**: Invalid request body or validation errors
- **401 Unauthorized**: Invalid or missing JWT token
- **403 Forbidden**: Valid token but attempting to access another user's data
- **404 Not Found**: Requested resource does not exist
- **409 Conflict**: Resource already exists (e.g., duplicate email)
- **422 Unprocessable Entity**: Invalid data format
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server-side error

## Development Guidelines

- Follow the specifications in `specs/` directory
- All API endpoints must enforce JWT authentication
- All endpoints must validate user ownership
- Write tests for all new features
- Use SQLModel for all database operations
- Never expose sensitive information in error messages

## References

- **API Specification**: `../specs/api/rest-endpoints.md`
- **Database Schema**: `../specs/database/schema.md`
- **Authentication Spec**: `../specs/authentication/spec.md`
- **Task CRUD Spec**: `../specs/task-crud/spec.md`

## Troubleshooting

### Database Connection Issues

If you encounter database connection errors:
1. Verify your `DATABASE_URL` is correct in `.env`
2. Ensure your Neon database is running and accessible
3. Check that your IP is whitelisted in Neon dashboard

### JWT Token Issues

If authentication fails:
1. Verify `BETTER_AUTH_SECRET` matches between frontend and backend
2. Check that the token is being sent in the `Authorization: Bearer <token>` header
3. Ensure the token hasn't expired

### Import Errors

If you see import errors:
1. Ensure you're in the virtual environment: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Verify you're running from the `backend/` directory

## Support

For issues or questions, refer to the project documentation in the `specs/` directory or check the project constitution at `.specify/memory/constitution.md`.
