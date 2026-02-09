# API Contract: User Authentication & JWT

## Authentication Endpoints

### POST /api/signup
**Purpose**: Register a new user account

**Request**:
- Method: POST
- Path: /api/signup
- Content-Type: application/json
- Headers: None required
- Body:
  ```json
  {
    "email": "string (required, valid email format)",
    "password": "string (required, minimum 8 chars with uppercase, lowercase, number)",
    "name": "string (required, user display name)"
  }
  ```

**Response**:
- Success (201 Created):
  ```json
  {
    "user": {
      "id": "string",
      "email": "string",
      "name": "string",
      "createdAt": "string (ISO 8601 timestamp)"
    },
    "token": "string (JWT token)"
  }
  ```

**Error Responses**:
- 400 Bad Request: Invalid request body, weak password, invalid email format
- 409 Conflict: Email already exists

### POST /api/signin
**Purpose**: Authenticate existing user and return JWT token

**Request**:
- Method: POST
- Path: /api/signin
- Content-Type: application/json
- Headers: None required
- Body:
  ```json
  {
    "email": "string (required, valid email format)",
    "password": "string (required)"
  }
  ```

**Response**:
- Success (200 OK):
  ```json
  {
    "user": {
      "id": "string",
      "email": "string",
      "name": "string",
      "createdAt": "string (ISO 8601 timestamp)"
    },
    "token": "string (JWT token)"
  }
  ```

**Error Responses**:
- 400 Bad Request: Invalid request body
- 401 Unauthorized: Invalid credentials (incorrect email or password)

## Protected Task Endpoints

### Authorization Requirements
All the following endpoints require:
- Header: `Authorization: Bearer <JWT token>`
- Token must be valid (not expired, proper signature)
- Token user_id must match the user_id in the URL path

### GET /api/{user_id}/tasks
**Purpose**: Retrieve all tasks for a specific user

**Request**:
- Method: GET
- Path: /api/{user_id}/tasks
- Headers: `Authorization: Bearer <JWT token>`
- Query Parameters (optional):
  - page: Page number for pagination (default: 1)
  - limit: Number of tasks per page (default: 20, max: 100)
  - status: Filter by completion status ('completed', 'pending', 'all')

**Response**:
- Success (200 OK):
  ```json
  {
    "tasks": [
      {
        "taskId": "string",
        "userId": "string",
        "title": "string",
        "description": "string",
        "completed": "boolean",
        "priority": "low|medium|high",
        "dueDate": "string (ISO 8601)",
        "createdAt": "string (ISO 8601)",
        "updatedAt": "string (ISO 8601)"
      }
    ],
    "pagination": {
      "currentPage": "number",
      "totalPages": "number",
      "totalTasks": "number",
      "hasNextPage": "boolean",
      "hasPreviousPage": "boolean"
    }
  }
  ```

**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: Token user_id does not match URL user_id
- 422 Unprocessable Entity: Invalid user_id format

### POST /api/{user_id}/tasks
**Purpose**: Create a new task for a specific user

**Request**:
- Method: POST
- Path: /api/{user_id}/tasks
- Headers: `Authorization: Bearer <JWT token>`, `Content-Type: application/json`
- Body:
  ```json
  {
    "title": "string (required, 1-255 characters)",
    "description": "string (optional, 0-1000 characters)",
    "priority": "string (optional, one of: 'low', 'medium', 'high'; default: 'medium')",
    "dueDate": "string (optional, ISO 8601 format)"
  }
  ```

**Response**:
- Success (201 Created):
  ```json
  {
    "taskId": "string",
    "userId": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean (false)",
    "priority": "low|medium|high",
    "dueDate": "string (ISO 8601)",
    "createdAt": "string (ISO 8601)",
    "updatedAt": "string (ISO 8601)"
  }
  ```

**Error Responses**:
- 400 Bad Request: Invalid request body or validation errors
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: Token user_id does not match URL user_id
- 422 Unprocessable Entity: Invalid user_id format or validation errors

### GET /api/{user_id}/tasks/{id}
**Purpose**: Retrieve a specific task by ID for a user

**Request**:
- Method: GET
- Path: /api/{user_id}/tasks/{id}
- Headers: `Authorization: Bearer <JWT token>`

**Response**:
- Success (200 OK):
  ```json
  {
    "taskId": "string",
    "userId": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "priority": "low|medium|high",
    "dueDate": "string (ISO 8601)",
    "createdAt": "string (ISO 8601)",
    "updatedAt": "string (ISO 8601)"
  }
  ```

**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: Token user_id does not match URL user_id
- 404 Not Found: Task not found
- 422 Unprocessable Entity: Invalid user_id or task_id format

### PUT /api/{user_id}/tasks/{id}
**Purpose**: Update an existing task for a user

**Request**:
- Method: PUT
- Path: /api/{user_id}/tasks/{id}
- Headers: `Authorization: Bearer <JWT token>`, `Content-Type: application/json`
- Body:
  ```json
  {
    "title": "string (required, 1-255 characters)",
    "description": "string (optional, 0-1000 characters)",
    "priority": "string (optional, one of: 'low', 'medium', 'high')",
    "dueDate": "string (optional, ISO 8601 format)"
  }
  ```

**Response**:
- Success (200 OK):
  ```json
  {
    "taskId": "string",
    "userId": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "priority": "low|medium|high",
    "dueDate": "string (ISO 8601)",
    "createdAt": "string (ISO 8601)",
    "updatedAt": "string (ISO 8601)"
  }
  ```

**Error Responses**:
- 400 Bad Request: Invalid request body or validation errors
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: Token user_id does not match URL user_id
- 404 Not Found: Task not found
- 422 Unprocessable Entity: Invalid user_id or task_id format

### DELETE /api/{user_id}/tasks/{id}
**Purpose**: Delete a specific task for a user

**Request**:
- Method: DELETE
- Path: /api/{user_id}/tasks/{id}
- Headers: `Authorization: Bearer <JWT token>`

**Response**:
- Success (204 No Content): No response body

**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: Token user_id does not match URL user_id
- 404 Not Found: Task not found
- 422 Unprocessable Entity: Invalid user_id or task_id format

### PATCH /api/{user_id}/tasks/{id}/complete
**Purpose**: Toggle the completion status of a task

**Request**:
- Method: PATCH
- Path: /api/{user_id}/tasks/{id}/complete
- Headers: `Authorization: Bearer <JWT token>`, `Content-Type: application/json`
- Body:
  ```json
  {
    "completed": "boolean (required)"
  }
  ```

**Response**:
- Success (200 OK):
  ```json
  {
    "taskId": "string",
    "userId": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "priority": "low|medium|high",
    "dueDate": "string (ISO 8601)",
    "createdAt": "string (ISO 8601)",
    "updatedAt": "string (ISO 8601)"
  }
  ```

**Error Responses**:
- 400 Bad Request: Invalid request body or validation errors
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: Token user_id does not match URL user_id
- 404 Not Found: Task not found
- 422 Unprocessable Entity: Invalid user_id or task_id format

## JWT Validation Requirements

### Token Format
- Header: `Authorization: Bearer <token>`
- Token must be a valid JWT with proper structure
- Algorithm: HS256
- Secret: BETTER_AUTH_SECRET environment variable

### Claims Validation
- `sub` (subject): Must contain user ID
- `exp` (expiration): Must not be in the past
- Signature: Must be valid using the shared secret

### Authorization Enforcement
- Token user_id must match the user_id in the URL path
- Invalid tokens return 401 Unauthorized
- Valid token with wrong user_id returns 403 Forbidden