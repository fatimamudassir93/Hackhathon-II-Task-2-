# Multi-Provider LLM System

## Overview

The backend has been refactored to support multiple LLM providers instead of being locked to OpenAI Agents SDK. You can now choose between:

- **OpenAI** (GPT-4, GPT-3.5)
- **Groq** (Llama 3.1, Mixtral, Gemma)
- **Google Gemini** (Gemini 1.5 Pro, Gemini 1.5 Flash)

## Architecture

### Components

1. **Provider Abstraction Layer** (`src/llm/`)
   - `base.py` - Abstract base class for all providers
   - `openai_provider.py` - OpenAI API implementation
   - `groq_provider.py` - Groq API implementation (OpenAI-compatible)
   - `gemini_provider.py` - Google Gemini API implementation
   - `provider_factory.py` - Factory for creating provider instances

2. **Tool System** (`src/llm/tool_registry.py`)
   - Decorator-based tool registration
   - Automatic JSON schema generation from function signatures
   - Provider-agnostic tool definitions

3. **Agent System** (`src/llm/agent.py`)
   - `Agent` - Agent definition with instructions and tools
   - `AgentContext` - Context passed to tool functions (db_session, user_id)
   - `AgentRunner` - Orchestrates multi-turn conversations with tool calling

4. **Routing** (`src/agents/triage.py`)
   - Keyword-based routing to specialist agents
   - Task, Tag, Reminder, and Analytics agents

## Configuration

### Environment Variables

```bash
# Choose your provider
LLM_PROVIDER=groq  # Options: openai, groq, gemini

# API Keys (provide the key for your chosen provider)
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=...

# Model Names (optional, defaults provided)
OPENAI_MODEL=gpt-4-turbo-preview
GROQ_MODEL=llama-3.1-70b-versatile
GEMINI_MODEL=gemini-1.5-pro
```

### Recommended Models

**Groq (Fast & Free Tier Available)**
- `llama-3.1-70b-versatile` - Best for general tasks
- `llama-3.1-8b-instant` - Fastest, good for simple tasks
- `mixtral-8x7b-32768` - Good for complex reasoning

**Gemini (Free Tier Available)**
- `gemini-1.5-pro` - Best quality
- `gemini-1.5-flash` - Faster, still high quality

**OpenAI (Paid)**
- `gpt-4-turbo-preview` - Best quality
- `gpt-3.5-turbo` - Faster, cheaper

## Installation

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the backend:
```bash
uvicorn src.main:app --reload
```

## Tool Registration

Tools are registered using the `@tool_registry.register()` decorator:

```python
from ..llm.tool_registry import tool_registry

@tool_registry.register(
    name="add_task",
    description="Add a new task for the user",
    parameters={
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Task title"},
            "description": {"type": "string", "description": "Optional description"}
        },
        "required": ["title"]
    }
)
async def add_task(ctx, title: str, description: str = None) -> dict:
    """Add a new task"""
    db_session = ctx.db_session
    user_id = ctx.user_id
    # ... implementation
    return {"task_id": task.id, "status": "created"}
```

## Agent Definition

Agents are defined with instructions and tool lists:

```python
from ..llm.agent import Agent
from ..llm.tool_registry import tool_registry

task_agent = Agent(
    name="Task Agent",
    instructions="You are a task management assistant...",
    tools=["add_task", "list_tasks", "update_task"],
    tool_registry=tool_registry
)
```

## Chat Flow

1. User sends message via POST `/api/{user_id}/chat`
2. `ChatService.process_message()` is called
3. Message is saved to conversation history
4. Recent conversation history is loaded (last 20 messages)
5. Message is routed to appropriate agent via `get_agent_for_message()`
6. `AgentRunner` executes the agent with the LLM provider
7. Agent may call tools multiple times (up to 10 turns)
8. Final response is saved and returned to user

## Migration from OpenAI Agents SDK

### What Changed

**Before (OpenAI Agents SDK):**
```python
from agents import Agent, function_tool, Runner, RunContextWrapper

@function_tool
async def add_task(ctx: RunContextWrapper, user_id: str, title: str):
    db_session = ctx.context["db_session"]
    # ...

agent = Agent(
    name="Task Agent",
    instructions="...",
    tools=[add_task]
)

result = await Runner.run(agent, input=messages, context=context)
```

**After (Multi-Provider):**
```python
from ..llm.tool_registry import tool_registry
from ..llm.agent import Agent, AgentRunner, AgentContext

@tool_registry.register(name="add_task", description="...", parameters={...})
async def add_task(ctx, title: str):
    db_session = ctx.db_session
    user_id = ctx.user_id
    # ...

agent = Agent(
    name="Task Agent",
    instructions="...",
    tools=["add_task"],
    tool_registry=tool_registry
)

provider = get_default_provider()
runner = AgentRunner(provider=provider)
context = AgentContext(db_session=db_session, user_id=user_id)
result = await runner.run(agent, messages=messages, context=context)
```

### Key Differences

1. **Tool Registration**: Use `@tool_registry.register()` decorator instead of `@function_tool`
2. **Context**: `AgentContext` object instead of `RunContextWrapper`
3. **Agent Tools**: Pass tool names (strings) instead of function references
4. **Provider**: Explicitly create provider and runner
5. **No user_id in tools**: Context already contains user_id

## Testing

Test with different providers by changing `LLM_PROVIDER` in `.env`:

```bash
# Test with Groq
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...

# Test with Gemini
LLM_PROVIDER=gemini
GEMINI_API_KEY=...

# Test with OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

## Troubleshooting

**Error: "GROQ_API_KEY is required"**
- Make sure you've set the API key for your chosen provider in `.env`

**Error: "Unsupported provider"**
- Check that `LLM_PROVIDER` is set to one of: `openai`, `groq`, `gemini`

**Tool calls not working**
- Verify tools are imported in agent files (triggers registration)
- Check tool parameter schemas match function signatures

**Gemini-specific issues**
- Gemini has different message format requirements
- System instructions are handled separately
- Tool responses use `function_response` format

## Performance Tips

1. **Use Groq for speed**: Groq has the fastest inference times
2. **Use Gemini for cost**: Gemini has generous free tier
3. **Use OpenAI for quality**: GPT-4 has best reasoning capabilities
4. **Adjust max_turns**: Lower for simple tasks, higher for complex multi-step operations
5. **Optimize context**: Only load necessary conversation history

## Future Enhancements

- [ ] Add support for Anthropic Claude
- [ ] Add support for local models (Ollama, LM Studio)
- [ ] Implement streaming responses
- [ ] Add caching for repeated tool calls
- [ ] Add metrics and monitoring
- [ ] Implement handoff system for agent-to-agent routing
