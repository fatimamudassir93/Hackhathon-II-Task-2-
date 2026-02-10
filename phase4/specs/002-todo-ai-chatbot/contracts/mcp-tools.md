# MCP Tool Contracts

**Branch**: `002-todo-ai-chatbot` | **Date**: 2026-02-08

All tools are Python functions registered with the OpenAI Agents SDK
via `@function_tool` decorator. Each tool receives `user_id` as the
first parameter for ownership enforcement.

## Task Tools (Task Agent)

### add_task

```python
add_task(user_id: str, title: str, description: str | None = None) -> dict
```

**Returns**: `{"task_id": str, "status": "created"}`
**Errors**: title empty → `{"error": "Title is required"}`

### list_tasks

```python
list_tasks(user_id: str, status: str | None = None) -> dict
```

**Parameters**: status = "pending" | "completed" | None (all)
**Returns**: `{"tasks": [{"id", "title", "completed", "priority", "due_date"}]}`

### update_task

```python
update_task(user_id: str, task_id: str, title: str | None = None, description: str | None = None) -> dict
```

**Returns**: `{"task_id": str, "status": "updated"}`
**Errors**: task not found → `{"error": "Task not found"}`

### complete_task

```python
complete_task(user_id: str, task_id: str) -> dict
```

**Returns**: `{"task_id": str, "status": "completed"}`
**Errors**: task not found → `{"error": "Task not found"}`

### delete_task

```python
delete_task(user_id: str, task_id: str) -> dict
```

**Returns**: `{"task_id": str, "status": "deleted"}`
**Errors**: task not found → `{"error": "Task not found"}`

## Reminder Tools (Reminder Agent)

### schedule_reminder

```python
schedule_reminder(user_id: str, task_id: str, remind_at: str) -> dict
```

**Parameters**: remind_at = ISO 8601 datetime string
**Returns**: `{"reminder_id": str, "status": "scheduled"}`
**Errors**:
- task not found → `{"error": "Task not found"}`
- past datetime → `{"error": "Reminder time must be in the future"}`

### cancel_reminder

```python
cancel_reminder(user_id: str, reminder_id: str) -> dict
```

**Returns**: `{"reminder_id": str, "status": "cancelled"}`
**Errors**: reminder not found → `{"error": "Reminder not found"}`

### list_reminders

```python
list_reminders(user_id: str) -> dict
```

**Returns**: `{"reminders": [{"id", "task_id", "remind_at", "status"}]}`

## Tag Tools (Tag/Category Agent)

### add_tag

```python
add_tag(user_id: str, task_id: str, tag: str) -> dict
```

**Returns**: `{"task_id": str, "tags": [str]}`
**Errors**:
- task not found → `{"error": "Task not found"}`
- tag empty → `{"error": "Tag name is required"}`

### remove_tag

```python
remove_tag(user_id: str, task_id: str, tag: str) -> dict
```

**Returns**: `{"task_id": str, "tags": [str]}`
**Errors**: tag not on task → `{"error": "Tag not found on task"}`

### list_tags

```python
list_tags(user_id: str) -> dict
```

**Returns**: `{"tags": [str]}`

### filter_tasks_by_tag

```python
filter_tasks_by_tag(user_id: str, tag: str) -> dict
```

**Returns**: `{"tasks": [{"id", "title", "completed", "priority"}], "tag": str}`

## Analytics Tools (Analytics Agent)

### count_tasks

```python
count_tasks(user_id: str) -> dict
```

**Returns**: `{"total": int}`

### tasks_done

```python
tasks_done(user_id: str) -> dict
```

**Returns**: `{"completed": int}`

### tasks_pending

```python
tasks_pending(user_id: str) -> dict
```

**Returns**: `{"pending": int}`
