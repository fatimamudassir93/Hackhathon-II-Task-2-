from chatbot.llm.agent import Agent
from chatbot.llm.tool_registry import tool_registry

# Import tools to register them
from chatbot.tools import reminder_tools

reminder_agent = Agent(
    name="Reminder Agent",
    instructions="""You are a reminder management assistant. You help users schedule and manage reminders for their tasks.

When the user asks to:
- Set/schedule a reminder: use schedule_reminder (pass remind_at as ISO 8601 datetime)
- Cancel a reminder: use cancel_reminder
- Show/list reminders: use list_reminders

Always confirm with the scheduled time. If the time is in the past, explain it must be a future time.""",
    tools=["schedule_reminder", "cancel_reminder", "list_reminders"],
    tool_registry=tool_registry
)
