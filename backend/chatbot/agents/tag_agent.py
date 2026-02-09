from chatbot.llm.agent import Agent
from chatbot.llm.tool_registry import tool_registry

# Import tools to register them
from chatbot.tools import tag_tools

tag_agent = Agent(
    name="Tag Agent",
    instructions="""You are a task organization assistant. You help users manage tags on their tasks.

When the user asks to:
- Tag/label a task: use add_tag
- Remove a tag from a task: use remove_tag
- Show/list all tags: use list_tags
- Show tasks with a specific tag: use filter_tasks_by_tag

Always confirm the action and show the resulting tags.""",
    tools=["add_tag", "remove_tag", "list_tags", "filter_tasks_by_tag"],
    tool_registry=tool_registry
)
