# REST API Endpoints Specification

## Feature Overview
- **Feature Name**: Task CRUD API Endpoints with Authentication
- **Phase**: II
- **Description**: RESTful API endpoints for Task operations with secure authentication and JWT enforcement
- **Dependencies**: Database persistence, Cryptographic libraries

## Authentication Endpoints

### POST /api/signup
- **Purpose**: Register a new user account
- **Method**: POST
- **Headers**:
  - `Content-Type: application/json` (required)
- **Request Body**:
  ```json
  {
    "email": "string (required, valid email format)",
    "password": "string (required, minimum 8 characters with uppercase, lowercase, and number)",
    "name": "string (required, user display name)"
  }
  ```
- **Response**:
  - **Success (201)**:
    ```json
    {
      "user": {
        "id": "string",
        "email": "string",
        "name": "string",
        "createdAt": "string (ISO 8601)"
      },
      "token": "string (JWT token)"
    }
    ```
- **Error Responses**:
  - **400**: Invalid request body or validation errors (weak password, invalid email)
  - **409**: Email already exists

### POST /api/signin
- **Purpose**: Authenticate existing user and return JWT token
- **Method**: POST
- **Headers**:
  - `Content-Type: application/json` (required)
- **Request Body**:
  ```json
  {
    "email": "string (required, valid email format)",
    "password": "string (required)"
  }
  ```
- **Response**:
  - **Success (200)**:
    ```json
    {
      "user": {
        "id": "string",
        "email": "string",
        "name": "string",
        "createdAt": "string (ISO 8601)"
      },
      "token": "string (JWT token)"
    }
    ```
- **Error Responses**:
  - **400**: Invalid request body
  - **401**: Invalid credentials (incorrect email or password)

## Protected Task Endpoints

### GET /api/{user_id}/tasks
- **Purpose**: Retrieve all tasks for a specific user
- **Method**: GET
- **Path Parameters**:
  - `{user_id}`: The ID of the user whose tasks to retrieve
- **Headers**:
  - `Authorization: Bearer <JWT>` (required)
- **Query Parameters**:
  - `page` (optional): Page number for pagination (default: 1)
  - `limit` (optional): Number of tasks per page (default: 20, max: 100)
  - `status` (optional): Filter by completion status ('completed', 'pending', 'all')
- **Request Body**: None
- **Response**:
  - **Success (200)**:
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
- **Error Responses**:
  - **401**: Invalid or missing JWT token
  - **403**: Token user_id does not match URL user_id
  - **422**: Invalid user_id format

### POST /api/{user_id}/tasks
- **Purpose**: Create a new task for a specific user
- **Method**: POST
- **Path Parameters**:
  - `{user_id}`: The ID of the user creating the task
- **Headers**:
  - `Authorization: Bearer <JWT>` (required)
  - `Content-Type: application/json` (required)
- **Request Body**:
  ```json
  {
    "title": "string (required, 1-255 characters)",
    "description": "string (optional, 0-1000 characters)",
    "priority": "string (optional, one of: 'low', 'medium', 'high'; default: 'medium')",
    "dueDate": "string (optional, ISO 8601 format)"
  }
  ```
- **Response**:
  - **Success (201)**:
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
- **Error Responses**:
  - **400**: Invalid request body or validation errors
  - **401**: Invalid or missing JWT token
  - **403**: Token user_id does not match URL user_id
  - **422**: Invalid user_id format or validation errors

### GET /api/{user_id}/tasks/{id}
- **Purpose**: Retrieve a specific task by ID for a user
- **Method**: GET
- **Path Parameters**:
  - `{user_id}`: The ID of the user who owns the task
  - `{id}`: The ID of the task to retrieve
- **Headers**:
  - `Authorization: Bearer <JWT>` (required)
- **Request Body**: None
- **Response**:
  - **Success (200)**:
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
- **Error Responses**:
  - **401**: Invalid or missing JWT token
  - **403**: Token user_id does not match URL user_id
  - **404**: Task not found
  - **422**: Invalid user_id or task_id format

### PUT /api/{user_id}/tasks/{id}
- **Purpose**: Update an existing task for a user
- **Method**: PUT
- **Path Parameters**:
  - `{user_id}`: The ID of the user who owns the task
  - `{id}`: The ID of the task to update
- **Headers**:
  - `Authorization: Bearer <JWT>` (required)
  - `Content-Type: application/json` (required)
- **Request Body**:
  ```json
  {
    "title": "string (required, 1-255 characters)",
    "description": "string (optional, 0-1000 characters)",
    "priority": "string (optional, one of: 'low', 'medium', 'high')",
    "dueDate": "string (optional, ISO 8601 format)"
  }
  ```
- **Response**:
  - **Success (200)**:
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
- **Error Responses**:
  - **400**: Invalid request body or validation errors
  - **401**: Invalid or missing JWT token
  - **403**: Token user_id does not match URL user_id
  - **404**: Task not found
  - **422**: Invalid user_id or task_id format

### DELETE /api/{user_id}/tasks/{id}
- **Purpose**: Delete a specific task for a user
- **Method**: DELETE
- **Path Parameters**:
  - `{user_id}`: The ID of the user who owns the task
  - `{id}`: The ID of the task to delete
- **Headers**:
  - `Authorization: Bearer <JWT>` (required)
- **Request Body**: None
- **Response**:
  - **Success (204)**: No content returned
- **Error Responses**:
  - **401**: Invalid or missing JWT token
  - **403**: Token user_id does not match URL user_id
  - **404**: Task not found
  - **422**: Invalid user_id or task_id format

### PATCH /api/{user_id}/tasks/{id}/complete
- **Purpose**: Toggle the completion status of a task
- **Method**: PATCH
- **Path Parameters**:
  - `{user_id}`: The ID of the user who owns the task
  - `{id}`: The ID of the task to update completion status
- **Headers**:
  - `Authorization: Bearer <JWT>` (required)
  - `Content-Type: application/json` (required)
- **Request Body**:
  ```json
  {
    "completed": "boolean (required)"
  }
  ```
- **Response**:
  - **Success (200)**:
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
- **Error Responses**:
  - **400**: Invalid request body or validation errors
  - **401**: Invalid or missing JWT token
  - **403**: Token user_id does not match URL user_id
  - **404**: Task not found
  - **422**: Invalid user_id or task_id format

## JWT Enforcement Requirements

### Token Validation
- All protected endpoints require a valid JWT token in the Authorization header
- Token must contain a user_id claim
- The user_id in the token must match the user_id in the URL path
- Tokens must not be expired
- Tokens must be properly signed and verifiable

### Authorization Enforcement
- Users can only access, modify, or delete their own tasks
- The system MUST verify that the authenticated user owns the requested resource
- Any mismatch between token user_id and URL user_id MUST result in a 403 Forbidden response
- Requests without valid JWT tokens MUST return 401 Unauthorized

## Validation Rules

### Request Validation
- All string fields must be properly encoded
- Dates must follow ISO 8601 format
- Priority values must be one of: 'low', 'medium', 'high'
- Task titles must be 1-255 characters
- Task descriptions must be 0-1000 characters
- User IDs and Task IDs must follow the system's identifier format
- Email addresses must follow standard validation
- Passwords must meet minimum strength requirements

### Response Validation
- All successful responses must return properly formatted JSON
- Timestamps must follow ISO 8601 format
- Error responses must follow the standard error format

## Error Format

Standard error response format:
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object (optional)"
  }
}
```

## Error Response Codes
- **401 Unauthorized**: Invalid or missing JWT token, or invalid credentials for signin
- **403 Forbidden**: Valid token but attempting to access another user's data
- **404 Not Found**: Requested resource does not exist
- **400 Bad Request**: Invalid request format or validation errors
- **409 Conflict**: Attempting to create a resource that already exists (e.g., duplicate email)

## References
- @specs/features/task-crud.md
- @specs/features/authentication.md
- @specs/database/schema.md