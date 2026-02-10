# TODO App AI Chatbot

This folder contains all the AI chatbot functionality for the TODO application. The chatbot uses a multi-agent architecture with support for multiple LLM providers.

## Structure

```
chatbot/
├── agents/           # Specialized agents for different tasks
│   ├── task_agent.py       # Handles task CRUD operations
│   ├── tag_agent.py        # Manages task tags
│   ├── reminder_agent.py   # Schedules and manages reminders
│   ├── analytics_agent.py  # Provides task statistics
│   └── triage.py          # Routes messages to appropriate agents
├── llm/             # LLM provider abstraction layer
│   ├── base.py            # Base provider interface
│   ├── openai_provider.py # OpenAI API integration
│   ├── groq_provider.py   # Groq API integration
│   ├── gemini_provider.py # Google Gemini integration
│   ├── provider_factory.py # Provider factory
│   ├── agent.py           # Agent runner and context
│   └── tool_registry.py   # Tool registration system
├── tools/           # Tool implementations for agents
│   ├── task_tools.py      # Task management tools
│   ├── tag_tools.py       # Tag management tools
│   ├── reminder_tools.py  # Reminder tools
│   └── analytics_tools.py # Analytics tools
├── routes/          # API endpoints
│   └── chat.py            # Chat endpoints
├── services/        # Business logic
│   ├── chat_service.py           # Main chat processing
│   └── conversation_service.py   # Conversation history
├── schemas/         # Pydantic models
│   └── chat.py            # Chat request/response schemas
├── models/          # Database models
│   └── conversation.py    # Conversation message model
└── tests/           # Test files
    ├── test_agents/
    ├── test_routes/
    ├── test_services/
    └── test_tools/
```

## Features

### Multi-Agent System
The chatbot uses specialized agents for different tasks:
- **Task Agent**: Create, list, update, complete, and delete tasks
- **Tag Agent**: Add/remove tags, list tags, filter tasks by tag
- **Reminder Agent**: Schedule and manage task reminders
- **Analytics Agent**: Get task statistics (count, completed, pending)

### Multi-Provider Support
Supports multiple LLM providers:
- **OpenAI**: GPT-3.5, GPT-4, etc.
- **Groq**: Fast inference with Llama, Mixtral models
- **Google Gemini**: Gemini Pro and other models

Configure the provider in `.env`:
```env
LLM_PROVIDER=openai  # or groq, gemini
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
```

### Tool Calling
Agents can call tools to perform actions:
- Tools are registered in `tool_registry`
- Each tool has a name, description, and parameter schema
- The LLM decides which tools to call based on user input

## API Endpoints

### Send Chat Message
```http
POST /api/{user_id}/chat
Content-Type: application/json
Authorization: Bearer <token>

{
  "message": "Add a task to buy groceries"
}
```

Response:
```json
{
  "reply": "I've added the task 'Buy groceries' for you.",
  "tool_calls": [
    {
      "tool": "add_task",
      "args": {"title": "Buy groceries"},
      "result": {"task_id": "123", "status": "created"}
    }
  ]
}
```

### Get Chat History
```http
GET /api/{user_id}/chat/history?limit=50&offset=0
Authorization: Bearer <token>
```

Response:
```json
{
  "messages": [
    {
      "id": "msg_1",
      "role": "user",
      "content": "Add a task to buy groceries",
      "created_at": "2024-02-08T10:00:00Z"
    },
    {
      "id": "msg_2",
      "role": "assistant",
      "content": "I've added the task 'Buy groceries' for you.",
      "tool_calls": "[...]",
      "created_at": "2024-02-08T10:00:01Z"
    }
  ],
  "total": 2
}
```

## Adding New Agents

1. Create a new agent file in `agents/`:
```python
from chatbot.llm.agent import Agent
from chatbot.llm.tool_registry import tool_registry
from chatbot.tools import your_tools

your_agent = Agent(
    name="Your Agent",
    instructions="Agent instructions...",
    tools=["tool1", "tool2"],
    tool_registry=tool_registry
)
```

2. Register tools in `tools/`:
```python
from chatbot.llm.tool_registry import tool_registry

@tool_registry.register(
    name="your_tool",
    description="Tool description",
    parameters={...}
)
async def your_tool(ctx, param1: str) -> dict:
    # Implementation
    return {"result": "success"}
```

3. Update triage logic in `agents/triage.py` to route to your agent.

## Adding New LLM Providers

1. Create a provider class in `llm/`:
```python
from chatbot.llm.base import BaseLLMProvider

class YourProvider(BaseLLMProvider):
    async def chat(self, messages, tools, temperature, max_tokens):
        # Implementation
        pass

    def format_tool_for_provider(self, tool):
        # Convert tool to provider format
        pass
```

2. Register in `llm/provider_factory.py`:
```python
elif provider_name == "your_provider":
    return YourProvider(api_key=api_key, model=model)
```

## Testing

Run tests:
```bash
pytest backend/chatbot/tests/
```

## Dependencies

- FastAPI
- SQLModel
- OpenAI SDK
- Groq SDK
- Google Generative AI SDK
- Pydantic

See `backend/requirements.txt` for full list.
