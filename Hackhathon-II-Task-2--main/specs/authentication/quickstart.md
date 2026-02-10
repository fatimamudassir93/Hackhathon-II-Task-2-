# Quickstart: User Authentication & JWT Implementation

## Prerequisites

### Environment Setup
1. Install required packages:
   ```bash
   pip install fastapi sqlmodel uvicorn bcrypt python-jose[cryptography] slowapi
   ```

2. Set environment variables:
   ```bash
   export BETTER_AUTH_SECRET="your-secret-key-here"
   export DATABASE_URL="postgresql+asyncpg://username:password@localhost/dbname"
   ```

### Database Preparation
1. Ensure Neon PostgreSQL database is accessible
2. Configure connection pooling settings
3. Prepare for SQLModel migrations

## Implementation Steps

### Step 1: Create User Model
1. Create `models/user.py` with SQLModel User class
2. Include all required fields (id, email, name, hashed_password, timestamps)
3. Add proper validation constraints
4. Implement password hashing helper methods

### Step 2: Implement Authentication Endpoints
1. Create `routes/auth.py` with signup and signin endpoints
2. Add input validation for email, password, and name
3. Implement password strength validation
4. Add JWT token generation using python-jose
5. Include proper error handling and responses

### Step 3: Create JWT Middleware
1. Develop middleware to extract and validate JWT tokens
2. Verify token signature and expiration
3. Attach authenticated user to request context
4. Handle token validation errors appropriately

### Step 4: Update Task Endpoints for Authorization
1. Modify existing task endpoints to validate user ownership
2. Check that JWT user_id matches URL user_id
3. Return 403 Forbidden for cross-user access attempts
4. Ensure all protected endpoints require valid JWT

### Step 5: Add Rate Limiting
1. Implement rate limiting on signup/signin endpoints
2. Use slowapi to limit requests per IP address
3. Return 429 status when limits exceeded

### Step 6: Testing
1. Write unit tests for authentication endpoints
2. Create integration tests for JWT validation
3. Verify user isolation (no cross-user access)
4. Test all error conditions and responses

## Running the Application

### Development
```bash
uvicorn main:app --reload
```

### API Testing
1. Test signup: `POST /api/signup`
2. Test signin: `POST /api/signin`
3. Test protected endpoints with JWT token
4. Verify authorization enforcement

## Configuration

### JWT Settings
- Token expiration: 24 hours
- Algorithm: HS256
- Secret: BETTER_AUTH_SECRET environment variable

### Rate Limiting
- 5 requests per minute per IP for auth endpoints
- Customizable based on deployment needs

## Security Considerations

### Password Storage
- Use bcrypt for password hashing
- Validate password strength (min 8 chars, upper/lower/num)
- Never store plain text passwords

### Token Security
- Use strong secret for JWT signing
- Validate token expiration on every request
- Verify token signature before processing

### Input Validation
- Validate email format
- Check password strength requirements
- Sanitize all user inputs

## Troubleshooting

### Common Issues
- JWT validation failures: Check that BETTER_AUTH_SECRET matches between frontend and backend
- Cross-user access: Verify that user_id in token matches user_id in URL
- Database connection: Ensure Neon PostgreSQL is accessible and credentials are correct
- Rate limiting: Verify slowapi is properly configured on auth endpoints