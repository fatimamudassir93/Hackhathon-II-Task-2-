from src.services.tag_service import TagService
from chatbot.llm.tool_registry import tool_registry


@tool_registry.register(
    name="add_tag",
    description="Add a tag to a task for organizing it.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {"type": "string", "description": "ID of the task to tag"},
            "tag": {"type": "string", "description": "Tag name to add"}
        },
        "required": ["task_id", "tag"]
    }
)
async def add_tag(ctx, task_id: str, tag: str) -> dict:
    """Add a tag to a task"""
    if not tag or not tag.strip():
        return {"error": "Tag name is required"}
    db_session = ctx.db_session
    user_id = ctx.user_id
    result = await TagService.add_tag_to_task(user_id, task_id, tag.strip(), db_session)
    return result


@tool_registry.register(
    name="remove_tag",
    description="Remove a tag from a task.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {"type": "string", "description": "ID of the task"},
            "tag": {"type": "string", "description": "Tag name to remove"}
        },
        "required": ["task_id", "tag"]
    }
)
async def remove_tag(ctx, task_id: str, tag: str) -> dict:
    """Remove a tag from a task"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    result = await TagService.remove_tag_from_task(user_id, task_id, tag.strip(), db_session)
    return result


@tool_registry.register(
    name="list_tags",
    description="List all unique tags used by the user.",
    parameters={"type": "object", "properties": {}}
)
async def list_tags(ctx) -> dict:
    """List all unique tags used by the user"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    tags = await TagService.get_tags_for_user(user_id, db_session)
    return {"tags": tags}


@tool_registry.register(
    name="filter_tasks_by_tag",
    description="Show all tasks that have a specific tag.",
    parameters={
        "type": "object",
        "properties": {
            "tag": {"type": "string", "description": "Tag name to filter by"}
        },
        "required": ["tag"]
    }
)
async def filter_tasks_by_tag(ctx, tag: str) -> dict:
    """Show all tasks that have a specific tag"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    result = await TagService.get_tasks_by_tag(user_id, tag.strip(), db_session)
    return result
