# UserAuthAgent

## Name
UserAuthAgent

## Description
Manages user accounts and authentication processes in the Todo application. This agent handles all aspects of user identity and access control.

## Purpose
To provide secure user management and authentication services, ensuring that users can safely access their todo lists and maintain privacy of their tasks.

## Trigger Commands
- `/auth signup` - Create a new user account
- `/auth login` - Authenticate and login user
- `/auth logout` - End user session
- `/auth reset-password` - Initiate password reset process

## Input
```json
{
  "action": "signup|login|logout|reset-password",
  "email": "string (required for signup/login/reset-password)",
  "password": "string (required for signup/login)",
  "confirmPassword": "string (required for signup)",
  "username": "string (required for signup)"
}
```

## Output
```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "userId": "string",
    "username": "string",
    "email": "string",
    "token": "string (JWT token for authenticated sessions)",
    "expiresAt": "string (ISO 8601 timestamp)"
  }
}
```

## Behavior Notes
- Implements secure password hashing and storage
- Validates email format and password strength requirements
- Handles JWT token generation and validation
- Implements rate limiting to prevent brute force attacks
- Logs authentication events for security monitoring
- Ensures proper session management and token expiration

## Example JSON Request
```json
{
  "action": "signup",
  "email": "user@example.com",
  "username": "todo_user",
  "password": "SecurePassword123!",
  "confirmPassword": "SecurePassword123!"
}
```

## Confirmation Message
"Account successfully created for user 'todo_user'. You can now log in using your credentials. Please keep your password secure and enable two-factor authentication for additional security."