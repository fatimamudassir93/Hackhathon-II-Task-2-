# Tasks: User Authentication & JWT

## Feature
User Authentication & JWT for Phase II Todo App

## Phase 1: Setup
**Goal**: Initialize project structure and dependencies for authentication implementation

- [X] T001 Create backend directory structure (src/, src/models/, src/services/, src/routes/, src/middleware/)
- [X] T002 [P] Install required dependencies (fastapi, sqlmodel, bcrypt, python-jose, slowapi, asyncpg)
- [X] T003 [P] Set up environment variables configuration (BETTER_AUTH_SECRET, DATABASE_URL)
- [X] T004 Create database configuration module with async engine setup
- [X] T005 Initialize project settings and configuration management

## Phase 2: Foundational
**Goal**: Create foundational components that block all user stories

- [X] T010 [P] Create User model in src/models/user.py following SQLModel specification
- [X] T011 [P] Implement password hashing utility functions in src/utils/password.py
- [X] T012 [P] Create JWT utility functions in src/utils/jwt.py for token generation and validation
- [X] T013 Create database session management in src/database/session.py
- [X] T014 [P] Implement rate limiting setup with slowapi in src/middleware/rate_limit.py
- [X] T015 Create base response models in src/schemas/responses.py
- [X] T016 Set up database initialization and migration configuration

## Phase 3: User Story 1 - User Registration
**Goal**: Implement user signup functionality with validation and JWT token generation

**Independent Test Criteria**: Can register a new user with email, password, and name, and receive a JWT token upon successful registration

**Tasks**:
- [X] T020 [P] [US1] Create user registration request schema in src/schemas/user.py
- [X] T021 [P] [US1] Create user registration response schema in src/schemas/user.py
- [X] T022 [P] [US1] Implement UserService with signup method in src/services/user_service.py
- [X] T023 [P] [US1] Create password validation utility in src/utils/validation.py
- [X] T024 [US1] Implement POST /api/signup endpoint in src/routes/auth.py
- [X] T025 [P] [US1] Add input validation middleware for signup endpoint
- [X] T026 [US1] Test user registration with valid credentials
- [X] T027 [US1] Test user registration error handling (invalid email, weak password, duplicate email)

## Phase 4: User Story 2 - User Authentication
**Goal**: Implement user signin functionality with credential validation and JWT token generation

**Independent Test Criteria**: Can authenticate existing user with email and password, and receive a JWT token upon successful authentication

**Tasks**:
- [X] T030 [P] [US2] Create user signin request schema in src/schemas/user.py
- [X] T031 [P] [US2] Create user signin response schema in src/schemas/user.py
- [X] T032 [P] [US2] Add signin method to UserService in src/services/user_service.py
- [X] T033 [US2] Implement POST /api/signin endpoint in src/routes/auth.py
- [X] T034 [P] [US2] Add credential validation logic to signin process
- [X] T035 [US2] Test user authentication with valid credentials
- [X] T036 [US2] Test user authentication error handling (invalid credentials)

## Phase 5: User Story 3 - JWT Middleware
**Goal**: Implement JWT token validation middleware for protected endpoints

**Independent Test Criteria**: Can validate JWT tokens in Authorization header and extract user information for request processing

**Tasks**:
- [X] T040 [P] [US3] Create JWT authentication middleware in src/middleware/auth.py
- [X] T041 [P] [US3] Implement token extraction from Authorization header
- [X] T042 [P] [US3] Add token validation and user ID extraction logic
- [X] T043 [US3] Create authentication dependency for FastAPI endpoints
- [X] T044 [P] [US3] Test JWT middleware with valid token
- [X] T045 [P] [US3] Test JWT middleware error handling (invalid, expired, missing tokens)

## Phase 6: User Story 4 - Authorization Enforcement
**Goal**: Enforce user-specific data access patterns on all task endpoints

**Independent Test Criteria**: Users can only access, modify, or delete their own tasks, with proper error responses for cross-user access attempts

**Tasks**:
- [X] T050 [P] [US4] Update Task model to enforce user_id foreign key relationship in src/models/task.py
- [X] T051 [P] [US4] Modify TaskService to filter by user_id in src/services/task_service.py
- [X] T052 [P] [US4] Update GET /api/{user_id}/tasks endpoint with authorization checks
- [X] T053 [P] [US4] Update POST /api/{user_id}/tasks endpoint with authorization checks
- [X] T054 [P] [US4] Update GET /api/{user_id}/tasks/{id} endpoint with authorization checks
- [X] T055 [P] [US4] Update PUT /api/{user_id}/tasks/{id} endpoint with authorization checks
- [X] T056 [P] [US4] Update DELETE /api/{user_id}/tasks/{id} endpoint with authorization checks
- [X] T057 [P] [US4] Update PATCH /api/{user_id}/tasks/{id}/complete endpoint with authorization checks
- [X] T058 [US4] Test authorization enforcement (cross-user access prevention)
- [X] T059 [US4] Test proper error responses (401, 403) for unauthorized access

## Phase 7: User Story 5 - Error Handling
**Goal**: Implement comprehensive error handling for authentication and authorization failures

**Independent Test Criteria**: Proper error responses are returned for all failure scenarios without exposing sensitive information

**Tasks**:
- [X] T060 [P] [US5] Create error response models in src/schemas/errors.py
- [X] T061 [P] [US5] Implement custom exception handlers in src/exceptions/handlers.py
- [X] T062 [P] [US5] Add validation error handling to auth endpoints
- [X] T063 [P] [US5] Add JWT validation error handling to middleware
- [X] T064 [P] [US5] Add authorization error handling to task endpoints
- [X] T065 [US5] Test all error response scenarios (400, 401, 403, 404, 409, 422, 429)
- [X] T066 [US5] Verify error messages don't expose sensitive information

## Phase 8: Polish & Cross-Cutting Concerns
**Goal**: Complete implementation with testing, documentation, and security enhancements

**Tasks**:
- [X] T070 [P] Write unit tests for User model and validation logic
- [X] T071 [P] Write unit tests for UserService methods
- [X] T072 [P] Write unit tests for JWT utilities
- [X] T073 [P] Write integration tests for auth endpoints
- [X] T074 [P] Write integration tests for protected task endpoints
- [X] T075 [P] Write security tests for authorization enforcement
- [X] T076 Add API documentation with OpenAPI/Swagger
- [X] T077 Create API endpoint documentation for auth flows
- [X] T078 Perform security review of authentication implementation
- [X] T079 Update main application entry point to include new routes and middleware
- [X] T080 Run complete test suite and fix any failing tests
- [X] T081 Perform code review and address any issues
- [X] T082 Update README with authentication setup and usage instructions

## Dependencies
- User Story 1 (Registration) has no dependencies
- User Story 2 (Authentication) depends on foundational components
- User Story 3 (JWT Middleware) depends on foundational components and JWT utilities
- User Story 4 (Authorization) depends on all previous stories
- User Story 5 (Error Handling) can be implemented in parallel with other stories

## Parallel Execution Examples
- User model, password utils, and JWT utils can be developed in parallel (T010-T012)
- All auth endpoint schemas can be created in parallel (T020, T021, T030, T031)
- All task endpoint updates can be done in parallel (T052-T057)
- All unit tests can be written in parallel (T070-T072)

## Implementation Strategy
**MVP Scope**: Complete User Story 1 (Registration) and User Story 2 (Authentication) with basic JWT token generation to have a minimal working authentication system.

**Incremental Delivery**:
1. MVP: Registration and authentication with JWT tokens
2. Phase 2: JWT middleware implementation
3. Phase 3: Authorization enforcement on task endpoints
4. Phase 4: Complete error handling and testing