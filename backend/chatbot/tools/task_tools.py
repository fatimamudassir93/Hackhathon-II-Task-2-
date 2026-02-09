from src.models.task import TaskCreate, TaskUpdate
from src.services.task_service import TaskService
from chatbot.llm.tool_registry import tool_registry


@tool_registry.register(
    name="add_task",
    description="Add a new task for the user. Use when the user wants to create a new todo item.",
    parameters={
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Task title (required)"},
            "description": {"type": "string", "description": "Optional task description"}
        },
        "required": ["title"]
    }
)
async def add_task(ctx, title: str, description: str = None) -> dict:
    """Add a new task for the user"""
    if not title or not title.strip():
        return {"error": "Title is required"}

    db_session = ctx.db_session
    user_id = ctx.user_id
    task_data = TaskCreate(title=title.strip(), description=description)
    task = await TaskService.create_task_for_user(task_data, user_id, db_session)
    return {"task_id": task.id, "status": "created", "title": task.title}


@tool_registry.register(
    name="list_tasks",
    description="List all tasks for the user. Optionally filter by status: 'pending' or 'completed'.",
    parameters={
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "Filter by status: 'pending' or 'completed'",
                "enum": ["pending", "completed"]
            }
        }
    }
)
async def list_tasks(ctx, status: str = None) -> dict:
    """List all tasks for the user"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    tasks = await TaskService.get_tasks_by_user_id(user_id, db_session)

    if status == "pending":
        tasks = [t for t in tasks if not t.completed]
    elif status == "completed":
        tasks = [t for t in tasks if t.completed]

    return {
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "completed": t.completed,
                "priority": t.priority,
                "due_date": str(t.due_date) if t.due_date else None,
            }
            for t in tasks
        ]
    }


@tool_registry.register(
    name="update_task",
    description="Update an existing task's title or description.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {"type": "string", "description": "ID of the task to update"},
            "title": {"type": "string", "description": "New title for the task"},
            "description": {"type": "string", "description": "New description for the task"}
        },
        "required": ["task_id"]
    }
)
async def update_task(ctx, task_id: str, title: str = None, description: str = None) -> dict:
    """Update an existing task"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    update_data = TaskUpdate()

    if title is not None:
        update_data.title = title.strip()
    if description is not None:
        update_data.description = description

    task = await TaskService.update_task_for_user(task_id, update_data, user_id, db_session)
    if not task:
        return {"error": "Task not found"}
    return {"task_id": task.id, "status": "updated", "title": task.title}


@tool_registry.register(
    name="complete_task",
    description="Mark a task as completed.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {"type": "string", "description": "ID of the task to complete"}
        },
        "required": ["task_id"]
    }
)
async def complete_task(ctx, task_id: str) -> dict:
    """Mark a task as completed"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    task = await TaskService.update_task_completion_for_user(task_id, True, user_id, db_session)
    if not task:
        return {"error": "Task not found"}
    return {"task_id": task.id, "status": "completed", "title": task.title}


@tool_registry.register(
    name="delete_task",
    description="Delete a task permanently.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {"type": "string", "description": "ID of the task to delete"}
        },
        "required": ["task_id"]
    }
)
async def delete_task(ctx, task_id: str) -> dict:
    """Delete a task permanently"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    deleted = await TaskService.delete_task_for_user(task_id, user_id, db_session)
    if not deleted:
        return {"error": "Task not found"}
    return {"task_id": task_id, "status": "deleted"}
