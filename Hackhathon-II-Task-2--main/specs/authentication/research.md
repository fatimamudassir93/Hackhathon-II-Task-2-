# Research: User Authentication & JWT Implementation

## Decision 1: Database Connection Configuration
**Decision**: Use SQLModel with Neon PostgreSQL through async engine configuration
**Rationale**: This follows the technology binding in the constitution (SQLModel for ORM, Neon PostgreSQL for database)
**Details**:
- Use `SQLModel.async_engine.create_async_engine()` for async operations
- Configure connection pooling and SSL settings for Neon
- Use environment variables for connection string

**Alternatives considered**:
- Raw asyncpg connections (rejected - violates ORM responsibility)
- SQLAlchemy Core (rejected - violates SQLModel requirement)

## Decision 2: JWT Integration Between Better Auth and FastAPI
**Decision**: Use python-jose library to validate Better Auth JWT tokens in FastAPI
**Rationale**: Better Auth uses standard JWT format which can be validated by python-jose with the same secret
**Details**:
- Extract JWT from Authorization header in FastAPI middleware
- Use the same BETTER_AUTH_SECRET for validation
- Decode user_id from token payload for authorization checks

**Alternatives considered**:
- PyJWT library (similar functionality, python-jose chosen for async support)
- Custom validation (rejected - unnecessary complexity)
- Different auth library (rejected - violates Better Auth frontend requirement)

## Decision 3: Password Hashing Implementation
**Decision**: Use bcrypt library for password hashing
**Rationale**: bcrypt is the industry standard for password hashing, well-established and secure
**Details**:
- Use `bcrypt.hashpw()` to hash passwords before storing
- Use `bcrypt.checkpw()` to verify passwords during signin
- Implement proper salt generation automatically handled by bcrypt

**Alternatives considered**:
- scrypt (also secure but bcrypt is more common)
- Argon2 (also secure but bcrypt has wider adoption)
- Custom hashing (rejected - security risk)

## Decision 4: Rate Limiting for Auth Endpoints
**Decision**: Use slowapi library for rate limiting
**Rationale**: slowapi is specifically designed for FastAPI and provides simple integration
**Details**:
- Implement rate limiting specifically on /api/signup and /api/signin endpoints
- Default to 5 attempts per minute per IP address
- Return 429 status code when limit exceeded

**Alternatives considered**:
- In-memory rate limiting (insufficient for production)
- Redis-based rate limiting (overhead for Phase II scope)
- Custom rate limiting (rejected - slowapi is purpose-built for this)

## Decision 5: JWT Token Configuration
**Decision**: Set JWT expiration to 24 hours as specified in functional requirements
**Rationale**: Matches the specification requirement and provides reasonable session duration
**Details**:
- Set 'exp' claim to 24 hours from issuance
- Use HS256 algorithm for signing
- Include 'iat' (issued at) and 'sub' (subject/user_id) claims

**Alternatives considered**:
- Shorter expiration (increases security but user friction)
- Longer expiration (convenient but less secure)
- Refresh tokens (out of Phase II scope)

## Decision 6: Error Response Format
**Decision**: Use standard error response format as defined in API specification
**Rationale**: Consistency with existing API design and clear error communication
**Details**:
- Format: { "error": { "code": "...", "message": "...", "details": "..." } }
- 401 for authentication failures
- 403 for authorization failures
- 400 for validation errors
- 409 for conflicts (duplicate email)

**Alternatives considered**:
- Different error formats (rejected - need consistency)
- HTTP status codes only (rejected - insufficient detail for clients)

## Technology Stack Confirmation
- **Frontend**: Next.js 16+ with Better Auth for authentication UI
- **Backend**: FastAPI with python-jose for JWT validation
- **ORM**: SQLModel for database models
- **Database**: Neon PostgreSQL
- **Password Hashing**: bcrypt
- **Rate Limiting**: slowapi
- **Environment**: BETTER_AUTH_SECRET for JWT validation