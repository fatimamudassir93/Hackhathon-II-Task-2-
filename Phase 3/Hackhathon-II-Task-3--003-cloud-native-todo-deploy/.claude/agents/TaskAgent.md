# TaskAgent

## Name
TaskAgent

## Description
Handles all task-related actions in the Todo application. This agent manages the complete lifecycle of tasks from creation to deletion.

## Purpose
To provide a centralized system for managing tasks in the Todo application, including creating, listing, updating, deleting, and marking tasks as completed.

## Trigger Commands
- `/task create` - Create a new task
- `/task list` - List all tasks
- `/task update` - Update an existing task
- `/task delete` - Delete a task
- `/task complete` - Mark a task as done

## Input
```json
{
  "action": "create|list|update|delete|complete",
  "taskId": "string (optional)",
  "title": "string (required for create/update)",
  "description": "string (optional)",
  "dueDate": "string (optional, ISO 8601 format)",
  "priority": "low|medium|high (optional)",
  "tags": ["string"] (optional)
}
```

## Output
```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "taskId": "string",
    "title": "string",
    "description": "string",
    "dueDate": "string",
    "priority": "low|medium|high",
    "completed": "boolean",
    "createdAt": "string (ISO 8601)",
    "updatedAt": "string (ISO 8601)"
  }
}
```

## Behavior Notes
- Validates input before processing any task action
- Ensures proper error handling for invalid task IDs or missing required fields
- Updates timestamps when tasks are modified
- Maintains data integrity by checking for duplicate tasks when appropriate
- Returns appropriate success/error messages based on the operation outcome

## Example JSON Request
```json
{
  "action": "create",
  "title": "Complete project proposal",
  "description": "Finish writing the project proposal document",
  "dueDate": "2026-01-15T10:00:00Z",
  "priority": "high",
  "tags": ["work", "urgent"]
}
```

## Confirmation Message
"Task 'Complete project proposal' has been successfully created with ID: task_abc123. You can update or delete this task using the provided ID."