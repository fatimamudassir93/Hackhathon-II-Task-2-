# Implementation Plan: User Authentication & JWT

## Technical Context

### Known Information
- **Feature**: User Authentication & JWT for Phase II Todo App
- **Frontend Stack**: Next.js 16+, TypeScript, Tailwind CSS, Better Auth
- **Backend Stack**: FastAPI, SQLModel, Neon PostgreSQL
- **Environment**: BETTER_AUTH_SECRET environment variable required
- **Spec Compliance**: Following @specs/features/authentication.md, @specs/database/schema.md, @specs/api/rest-endpoints.md
- **Constitution Compliance**: Following Phase II Todo Full-Stack Web Application Constitution

### Unknown Information
- **Database Connection Details**: NEEDS CLARIFICATION - Specific Neon PostgreSQL connection configuration
- **JWT Secret Configuration**: NEEDS CLARIFICATION - How BETTER_AUTH_SECRET is used with backend JWT validation
- **Password Hashing Algorithm**: NEEDS CLARIFICATION - Specific implementation details for bcrypt or equivalent
- **Rate Limiting Implementation**: NEEDS CLARIFICATION - Specific rate limiting mechanism for auth endpoints

## Constitution Check

### Technology Binding Adherence
- ✅ Frontend: Next.js 16+ with Better Auth for authentication UI
- ✅ Backend: FastAPI for REST API and JWT validation
- ✅ ORM: SQLModel for database models and queries
- ✅ Database: Neon Serverless PostgreSQL for user and task storage
- ✅ Responsibilities: Properly separated (no cross-layer mixing)

### Authentication Architecture Compliance
- ✅ User signs up/signs in via Better Auth frontend
- ✅ Better Auth issues JWT token
- ✅ Frontend attaches token as Authorization: Bearer <JWT>
- ✅ FastAPI backend extracts and verifies token using shared secret
- ✅ Backend compares JWT user_id with URL user_id
- ✅ Backend filters data by authenticated user_id

### Test-First Compliance
- ✅ All API endpoints will have authentication and authorization tests
- ✅ User isolation will be tested for cross-user access prevention
- ✅ All CRUD operations will have comprehensive test coverage

### REST API Contract Compliance
- ✅ All API routes will be under /api
- ✅ All protected endpoints will require JWT authentication
- ✅ All endpoints will enforce user ownership
- ✅ Proper error responses (401, 403) will be implemented

### Feature Scope Lock Compliance
- ✅ Implementation restricted to authorized features (signup, signin, JWT enforcement)
- ✅ No prohibited features will be included

### Spec-Driven Execution Compliance
- ✅ Will reference specs explicitly during implementation
- ✅ Will not invent API behavior, database fields, or UI flows

## Phase 0: Research

### Research Task 1: Database Connection Configuration
**Decision**: Determine specific Neon PostgreSQL connection setup for FastAPI/SQLModel
**Rationale**: Need to properly configure database connections for user authentication
**Alternatives considered**: Various connection pooling strategies, SSL settings

### Research Task 2: JWT Integration Between Better Auth and FastAPI
**Decision**: Determine how Better Auth JWT tokens will be validated by FastAPI backend
**Rationale**: Need to ensure frontend and backend use compatible JWT validation
**Alternatives considered**: Different JWT libraries, custom validation vs. existing solutions

### Research Task 3: Password Hashing Implementation
**Decision**: Select and implement secure password hashing algorithm (bcrypt or equivalent)
**Rationale**: Critical security requirement for user password storage
**Alternatives considered**: bcrypt, scrypt, Argon2

### Research Task 4: Rate Limiting for Auth Endpoints
**Decision**: Implement rate limiting to prevent brute force attacks
**Rationale**: Security requirement to protect authentication endpoints
**Alternatives considered**: In-memory vs. Redis-based rate limiting, different algorithms

## Phase 1: Design & Contracts

### Data Model: User Entity
- **userId** (string, PK): Unique identifier for the user
- **email** (string, UNIQUE): User's email address (used for authentication)
- **name** (string): User's display name
- **passwordHash** (string): Securely hashed password
- **createdAt** (timestamp): When account was created
- **updatedAt** (timestamp): When account was last modified

### Data Model: JWT Token Entity
- **token** (string): Encoded JWT token string
- **userId** (string): Embedded user identifier in token payload
- **expiration** (timestamp): Token expiration time
- **issuedAt** (timestamp): Token issuance time

### API Contracts
Based on @specs/api/rest-endpoints.md:

#### POST /api/signup
- **Purpose**: Register a new user account
- **Request Body**: {email, password, name}
- **Response**: {user: {...}, token: JWT}
- **Error Responses**: 400 (validation), 409 (duplicate email)

#### POST /api/signin
- **Purpose**: Authenticate existing user
- **Request Body**: {email, password}
- **Response**: {user: {...}, token: JWT}
- **Error Responses**: 400 (validation), 401 (invalid credentials)

#### Protected Task Endpoints
- **Authorization**: Bearer <JWT> in Authorization header
- **Validation**: JWT signature, expiration, user_id matching
- **Error Responses**: 401 (invalid token), 403 (cross-user access)

### Quickstart Guide
1. Set up environment variables (BETTER_AUTH_SECRET)
2. Configure database connection (Neon PostgreSQL)
3. Implement user model with SQLModel
4. Create auth endpoints (signup/signin)
5. Implement JWT middleware for protected routes
6. Add user ownership validation to task endpoints
7. Write tests for authentication flows
8. Verify cross-user access prevention

## Phase 2: Implementation Approach

### Step 1: Database Models
- Create User model using SQLModel with proper fields and constraints
- Implement proper password hashing before storing
- Ensure email uniqueness constraint

### Step 2: Authentication Endpoints
- Implement signup endpoint with input validation
- Implement signin endpoint with credential verification
- Generate JWT tokens upon successful authentication

### Step 3: JWT Middleware
- Create middleware to extract and validate JWT tokens
- Attach authenticated user to request context
- Verify token expiration and signature

### Step 4: Authorization Enforcement
- Update all task endpoints to validate user ownership
- Ensure user_id in token matches user_id in URL path
- Return appropriate error responses (401, 403)

### Step 5: Testing
- Unit tests for auth endpoints
- Integration tests for JWT validation
- Tests to verify cross-user access prevention
- Error condition tests

## Implementation Timeline
- Database models: 1 day
- Auth endpoints: 1-2 days
- JWT middleware: 1 day
- Authorization enforcement: 1 day
- Testing: 1-2 days
- Total estimated: 5-7 days

## Success Criteria
- Users can successfully register and sign in
- JWT tokens are properly issued and validated
- Users can only access their own tasks
- All security requirements are met
- Error handling works appropriately
- Tests pass with high coverage