# Database Schema Specification

## Feature Overview
- **Feature Name**: Task CRUD Database Schema
- **Phase**: II
- **Description**: Database schema for storing and retrieving user tasks
- **Dependencies**: None

## Database Schema

### Tables

#### users
- **Description**: Stores user information
- **Columns**:
  - `id` (VARCHAR(255), PRIMARY KEY): Unique identifier for the user
  - `email` (VARCHAR(255), UNIQUE, NOT NULL): User's email address
  - `name` (VARCHAR(255), NOT NULL): User's display name
  - `hashed_password` (TEXT, NOT NULL): Hashed password
  - `created_at` (TIMESTAMPTZ, DEFAULT CURRENT_TIMESTAMP): Account creation timestamp
  - `updated_at` (TIMESTAMPTZ, DEFAULT CURRENT_TIMESTAMP): Last update timestamp

#### tasks
- **Description**: Stores user tasks
- **Columns**:
  - `id` (VARCHAR(255), PRIMARY KEY): Unique identifier for the task
  - `user_id` (VARCHAR(255), NOT NULL): Reference to the owning user
  - `title` (VARCHAR(255), NOT NULL): Task title (1-255 characters)
  - `description` (TEXT, DEFAULT ''): Task description (up to 1000 characters)
  - `completed` (BOOLEAN, DEFAULT FALSE): Task completion status
  - `priority` (VARCHAR(20), DEFAULT 'medium'): Task priority ('low', 'medium', 'high')
  - `due_date` (TIMESTAMPTZ, NULLABLE): Optional deadline for the task
  - `created_at` (TIMESTAMPTZ, DEFAULT CURRENT_TIMESTAMP): Task creation timestamp
  - `updated_at` (TIMESTAMPTZ, DEFAULT CURRENT_TIMESTAMP): Last update timestamp

### Indexes
- `idx_tasks_user_id`: Index on `user_id` column in `tasks` table for efficient user-based queries
- `idx_tasks_completed`: Index on `completed` column in `tasks` table for filtering by completion status
- `idx_tasks_due_date`: Index on `due_date` column in `tasks` table for date-based queries
- `idx_tasks_priority`: Index on `priority` column in `tasks` table for priority-based queries

### Foreign Keys
- `fk_tasks_user_id`: Foreign key constraint linking `user_id` in `tasks` table to `id` in `users` table
  - ON DELETE CASCADE: When a user is deleted, all their tasks are also deleted
  - ON UPDATE CASCADE: When a user ID is updated, related task records are updated

### Constraints
- `chk_task_title_length`: Ensures task title is between 1 and 255 characters
- `chk_task_desc_length`: Ensures task description is between 0 and 1000 characters
- `chk_task_priority_values`: Ensures priority is one of 'low', 'medium', 'high'
- `chk_task_user_association`: Ensures every task is associated with a valid user
- `chk_user_email_unique`: Ensures email addresses are unique across users
- `chk_user_email_format`: Ensures email follows standard email format validation
- `chk_user_name_not_empty`: Ensures user name is not empty

## Ownership Constraints

### User-Task Association
- Each task MUST be associated with exactly one user through the `user_id` foreign key
- Users can only access tasks where `user_id` matches their own user ID
- The database schema enforces referential integrity through foreign key constraints
- Deletion of a user automatically removes all their tasks (CASCADE delete)

### Data Isolation
- The application layer MUST filter all queries by `user_id` to ensure users only see their own tasks
- Direct database access SHOULD be prevented through proper access controls
- All queries SHOULD include a `WHERE user_id = ?` clause for task-related operations

## Data Types

### String Types
- VARCHAR(255): For short text fields like user IDs, usernames, and task titles
- TEXT: For longer content like hashed passwords and task descriptions

### Date/Time Types
- TIMESTAMPTZ: For all date/time fields to handle timezone-aware timestamps

### Boolean Types
- BOOLEAN: For binary states like task completion status

## Performance Considerations

### Query Patterns
- Most common query: Retrieve all tasks for a specific user
- Secondary query: Filter tasks by completion status
- Tertiary query: Sort or filter by due date or priority

### Index Strategy
- Primary index on user_id to support user-based filtering
- Secondary indexes on frequently queried fields (completed, due_date, priority)
- Composite indexes may be added later based on query patterns

## Migration Strategy

### Initial Setup
- Create `users` table with all specified columns and constraints
- Create `tasks` table with all specified columns, constraints, and indexes
- Establish foreign key relationship between tables

### Future Expansion
- Additional columns can be added to existing tables using ALTER TABLE
- New indexes can be created as query patterns emerge
- Table partitioning may be considered for very large datasets

## References
- @specs/features/task-crud.md
- @specs/api/rest-endpoints.md
- @specs/auth/system.md