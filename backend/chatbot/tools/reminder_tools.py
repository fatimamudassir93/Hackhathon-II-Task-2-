from src.services.reminder_service import ReminderService
from chatbot.llm.tool_registry import tool_registry


@tool_registry.register(
    name="schedule_reminder",
    description="Schedule a reminder for a task at a specific date/time. remind_at must be ISO 8601 format.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {"type": "string", "description": "ID of the task to set reminder for"},
            "remind_at": {"type": "string", "description": "ISO 8601 datetime when to remind (e.g., '2024-12-25T10:00:00')"}
        },
        "required": ["task_id", "remind_at"]
    }
)
async def schedule_reminder(ctx, task_id: str, remind_at: str) -> dict:
    """Schedule a reminder for a task"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    result = await ReminderService.schedule_reminder(user_id, task_id, remind_at, db_session)
    return result


@tool_registry.register(
    name="cancel_reminder",
    description="Cancel an active reminder.",
    parameters={
        "type": "object",
        "properties": {
            "reminder_id": {"type": "string", "description": "ID of the reminder to cancel"}
        },
        "required": ["reminder_id"]
    }
)
async def cancel_reminder(ctx, reminder_id: str) -> dict:
    """Cancel an active reminder"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    result = await ReminderService.cancel_reminder(user_id, reminder_id, db_session)
    return result


@tool_registry.register(
    name="list_reminders",
    description="List all reminders for the user.",
    parameters={"type": "object", "properties": {}}
)
async def list_reminders(ctx) -> dict:
    """List all reminders for the user"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    result = await ReminderService.list_reminders_for_user(user_id, db_session)
    return result
