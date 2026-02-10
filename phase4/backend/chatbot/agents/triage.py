"""
Triage/routing logic for the chat system.

Since we don't have a handoff system in the new multi-provider architecture,
the chat service will handle routing directly based on keyword matching.
"""

from .task_agent import task_agent
from .tag_agent import tag_agent
from .reminder_agent import reminder_agent
from .analytics_agent import analytics_agent


def get_agent_for_message(message: str):
    """
    Route a user message to the appropriate specialist agent.

    Args:
        message: User's message text

    Returns:
        Agent instance to handle the message
    """
    message_lower = message.lower()

    # Task-related keywords
    task_keywords = [
        "add task", "create task", "new task", "make task",
        "list task", "show task", "view task", "my task",
        "update task", "edit task", "change task", "modify task",
        "complete task", "finish task", "done task", "mark task",
        "delete task", "remove task"
    ]

    # Tag-related keywords
    tag_keywords = [
        "add tag", "tag task", "label task",
        "remove tag", "untag",
        "list tag", "show tag", "my tag",
        "filter by tag", "tasks with tag"
    ]

    # Reminder-related keywords
    reminder_keywords = [
        "remind", "reminder", "schedule reminder",
        "set reminder", "cancel reminder", "list reminder"
    ]

    # Analytics-related keywords
    analytics_keywords = [
        "how many", "count", "total task",
        "completed task", "done task",
        "pending task", "remaining task"
    ]

    # Check for matches
    if any(keyword in message_lower for keyword in tag_keywords):
        return tag_agent
    elif any(keyword in message_lower for keyword in reminder_keywords):
        return reminder_agent
    elif any(keyword in message_lower for keyword in analytics_keywords):
        return analytics_agent
    else:
        # Default to task agent for most requests
        return task_agent
