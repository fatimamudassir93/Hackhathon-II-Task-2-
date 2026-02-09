# TagCategoryAgent

## Name
TagCategoryAgent

## Description
Organizes tasks using tags and categories in the Todo application. This agent manages the tagging system that allows users to categorize and filter their tasks effectively.

## Purpose
To provide a flexible tagging system that enables users to organize, categorize, and filter their tasks based on custom tags, improving task management and searchability.

## Trigger Commands
- `/tag add` - Add a tag to a task
- `/tag remove` - Remove a tag from a task
- `/tag list` - List all available tags
- `/tag filter` - Filter tasks by specific tags

## Input
```json
{
  "action": "add|remove|list|filter",
  "taskId": "string (required for add/remove)",
  "tag": "string (required for add/remove)",
  "userId": "string (required for list/filter)",
  "tags": ["string"] (required for filter)",
  "includeSubtasks": "boolean (optional, defaults to false)"
}
```

## Output
```json
{
  "success": "boolean",
  "message": "string",
  "data": {
    "tags": ["string"],
    "taskId": "string (for add/remove)",
    "filteredTasks": [
      {
        "taskId": "string",
        "title": "string",
        "tags": ["string"],
        "completed": "boolean"
      }
    ],
    "totalFilteredCount": "number"
  }
}
```

## Behavior Notes
- Validates tag format and length constraints
- Prevents duplicate tags on the same task
- Maintains alphabetical ordering of tags
- Supports hierarchical tagging if needed
- Implements efficient filtering algorithms for large task sets
- Handles tag suggestions based on user's previously used tags

## Example JSON Request
```json
{
  "action": "add",
  "taskId": "task_abc123",
  "tag": "work"
}
```

## Confirmation Message
"Tag 'work' successfully added to task 'task_abc123'. You can now filter tasks by this tag to quickly find related items. You have 12 tasks tagged with 'work' in total."