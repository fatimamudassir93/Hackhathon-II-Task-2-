from chatbot.llm.agent import Agent
from chatbot.llm.tool_registry import tool_registry

# Import tools to register them
from chatbot.tools import analytics_tools

analytics_agent = Agent(
    name="Analytics Agent",
    instructions="""You are a task analytics assistant. You help users understand their task statistics.

When the user asks:
- How many tasks they have: use count_tasks
- How many tasks are done/completed: use tasks_done
- How many tasks are pending/remaining: use tasks_pending

Provide clear, friendly responses with the numbers.""",
    tools=["count_tasks", "tasks_done", "tasks_pending"],
    tool_registry=tool_registry
)
