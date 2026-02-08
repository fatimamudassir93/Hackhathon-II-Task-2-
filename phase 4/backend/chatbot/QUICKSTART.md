# Quick Start Guide - Chatbot

## Prerequisites

1. Python 3.10+ installed
2. PostgreSQL database (Neon DB configured)
3. LLM API key (OpenAI, Groq, or Gemini)

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create or update `.env` file:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname

# Authentication
BETTER_AUTH_SECRET=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# LLM Provider (choose one)
LLM_PROVIDER=groq  # or openai, gemini

# API Keys (add the one matching your LLM_PROVIDER)
GROQ_API_KEY=your_groq_api_key
# OPENAI_API_KEY=your_openai_api_key
# GEMINI_API_KEY=your_gemini_api_key
```

### 3. Start the Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Testing the Chatbot

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  }'
```

### 2. Sign In

```bash
curl -X POST http://localhost:8000/api/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Save the `access_token` from the response.

### 3. Send a Chat Message

```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

### 4. Get Chat History

```bash
curl -X GET http://localhost:8000/api/{user_id}/chat/history \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Example Chat Commands

### Task Management
- "Add a task to buy groceries"
- "List all my tasks"
- "Update task 123 to 'Buy organic groceries'"
- "Complete task 123"
- "Delete task 123"

### Tag Management
- "Add tag 'urgent' to task 123"
- "Remove tag 'urgent' from task 123"
- "List all my tags"
- "Show tasks with tag 'urgent'"

### Reminders
- "Remind me about task 123 tomorrow at 10am"
- "Cancel reminder 456"
- "List all my reminders"

### Analytics
- "How many tasks do I have?"
- "How many tasks are completed?"
- "How many tasks are pending?"

## Chatbot Architecture

### Agents
The chatbot uses specialized agents:
- **Task Agent:** Handles task CRUD operations
- **Tag Agent:** Manages task tags
- **Reminder Agent:** Schedules reminders
- **Analytics Agent:** Provides statistics

### LLM Providers
Supports multiple providers:
- **OpenAI:** GPT-3.5, GPT-4
- **Groq:** Llama 3.1, Mixtral
- **Gemini:** Gemini Pro

### Tool System
15 tools available:
- 5 task tools
- 4 tag tools
- 3 reminder tools
- 3 analytics tools

## Troubleshooting

### Server won't start
- Check if port 8000 is available
- Verify DATABASE_URL is correct
- Check Python version (3.10+ required)

### Chat returns errors
- Verify LLM API key is set correctly
- Check LLM_PROVIDER matches the API key
- Ensure you have internet connection

### Database errors
- Verify PostgreSQL is running
- Check DATABASE_URL format
- Run migrations if needed

### Authentication errors
- Verify BETTER_AUTH_SECRET is set
- Check token hasn't expired
- Ensure user exists in database

## Development

### Running Tests

```bash
cd backend
pytest chatbot/tests/ -v
```

### Adding New Tools

1. Create tool function in `chatbot/tools/`
2. Register with `@tool_registry.register()`
3. Add to agent's tool list
4. Update triage logic if needed

### Adding New Agents

1. Create agent in `chatbot/agents/`
2. Define instructions and tools
3. Update `triage.py` routing logic
4. Add tests

## File Structure

```
backend/
├── chatbot/              # Chatbot module
│   ├── agents/          # AI agents
│   ├── llm/            # LLM providers
│   ├── tools/          # Tool implementations
│   ├── routes/         # API endpoints
│   ├── services/       # Business logic
│   ├── schemas/        # Pydantic models
│   ├── models/         # Database models
│   └── tests/          # Tests
└── src/                 # Core application
    ├── models/         # Core models
    ├── routes/         # Core routes
    └── services/       # Core services
```

## Documentation

- **README.md** - Full chatbot documentation
- **MIGRATION.md** - Migration details
- **TEST_REPORT.md** - Test results
- **QUICKSTART.md** - This guide

## Support

For issues or questions:
1. Check the documentation in `backend/chatbot/`
2. Review test reports
3. Check server logs for errors

## Next Steps

1. Configure your LLM API key
2. Start the server
3. Test the chat endpoints
4. Integrate with frontend
5. Add custom agents/tools as needed

---

**Ready to chat!** 🚀
