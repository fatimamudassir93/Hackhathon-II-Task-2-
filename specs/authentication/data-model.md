# Data Model: User Authentication & JWT

## User Entity

### Fields
- **id** (string, PRIMARY KEY)
  - Type: UUID string or auto-generated string ID
  - Constraints: Required, Unique
  - Purpose: Unique identifier for the user

- **email** (string)
  - Type: VARCHAR(255)
  - Constraints: Required, Unique, Valid email format
  - Purpose: User's email address used for authentication

- **name** (string)
  - Type: VARCHAR(255)
  - Constraints: Required, Not empty
  - Purpose: User's display name

- **hashed_password** (string)
  - Type: TEXT
  - Constraints: Required
  - Purpose: Securely hashed password using bcrypt

- **created_at** (timestamp)
  - Type: TIMESTAMPTZ
  - Default: Current timestamp
  - Purpose: When account was created

- **updated_at** (timestamp)
  - Type: TIMESTAMPTZ
  - Default: Current timestamp, auto-update
  - Purpose: When account was last modified

### Relationships
- One-to-many with Tasks entity (user has many tasks)
- Foreign key relationship: Task.user_id references User.id

### Validation Rules
- Email: Must match standard email format
- Name: Must be 1-255 characters, not empty
- Password: Stored as hashed value (validation occurs during signup/signin)

## JWT Token Structure

### Payload Claims
- **sub** (Subject)
  - Type: string (user ID)
  - Purpose: Identify the user the token refers to

- **exp** (Expiration Time)
  - Type: numeric date (Unix timestamp)
  - Purpose: When the token expires (24 hours from issuance)

- **iat** (Issued At)
  - Type: numeric date (Unix timestamp)
  - Purpose: When the token was issued

### Token Properties
- Algorithm: HS256
- Secret: BETTER_AUTH_SECRET environment variable
- Expiration: 24 hours from issuance

## Task Entity (Updated for User Ownership)

### Additional Validation
- Each task must have a user_id that corresponds to an existing user
- Users can only access tasks where task.user_id equals authenticated user's id

## State Transitions

### User Registration Flow
1. User provides email, password, name
2. System validates input
3. System hashes password
4. System creates User record
5. System generates JWT token
6. System returns success response with token

### Authentication Flow
1. User provides email and password
2. System validates credentials
3. System generates JWT token
4. System returns token and user profile
5. User includes token in Authorization header for subsequent requests

### Authorization Flow
1. Request includes Authorization: Bearer <token>
2. System validates JWT signature and expiration
3. System extracts user_id from token
4. System verifies user has access to requested resource
5. System processes request or returns 403 Forbidden