from src.services.task_service import TaskService
from chatbot.llm.tool_registry import tool_registry


@tool_registry.register(
    name="count_tasks",
    description="Count the total number of tasks for the user.",
    parameters={"type": "object", "properties": {}}
)
async def count_tasks(ctx) -> dict:
    """Count the total number of tasks for the user"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    tasks = await TaskService.get_tasks_by_user_id(user_id, db_session)
    return {"total": len(tasks)}


@tool_registry.register(
    name="tasks_done",
    description="Count the number of completed tasks for the user.",
    parameters={"type": "object", "properties": {}}
)
async def tasks_done(ctx) -> dict:
    """Count the number of completed tasks for the user"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    tasks = await TaskService.get_tasks_by_user_id(user_id, db_session)
    completed = [t for t in tasks if t.completed]
    return {"completed": len(completed)}


@tool_registry.register(
    name="tasks_pending",
    description="Count the number of pending (not completed) tasks for the user.",
    parameters={"type": "object", "properties": {}}
)
async def tasks_pending(ctx) -> dict:
    """Count the number of pending (not completed) tasks for the user"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    tasks = await TaskService.get_tasks_by_user_id(user_id, db_session)
    pending = [t for t in tasks if not t.completed]
    return {"pending": len(pending)}
