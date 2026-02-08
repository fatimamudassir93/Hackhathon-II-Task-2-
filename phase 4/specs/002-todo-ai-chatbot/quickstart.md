# Quickstart: Todo AI Chatbot

**Branch**: `002-todo-ai-chatbot` | **Date**: 2026-02-08

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Neon PostgreSQL account (database provisioned)
- OpenAI API key (for Agents SDK)

## 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with:
#   DATABASE_URL=postgresql+asyncpg://<neon-connection-string>
#   BETTER_AUTH_SECRET=<your-secret-min-32-bytes>
#   OPENAI_API_KEY=<your-openai-api-key>

# Run database migrations (tables created on startup)
uvicorn src.main:app --reload --port 8000
```

## 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with:
#   DATABASE_URL_NEON=<neon-connection-string>
#   BETTER_AUTH_SECRET=<same-secret-as-backend>
#   NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
```

## 3. Verify

1. Open `http://localhost:3000` — sign up / sign in
2. Navigate to the chat interface
3. Type "Add a task called Buy groceries"
4. Verify the task is created and confirmed in the chat
5. Type "Show my tasks" to see the task list
6. Type "Complete task 1" to mark it done

## Environment Variables

### Backend (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | yes | Neon PostgreSQL asyncpg URL |
| BETTER_AUTH_SECRET | yes | JWT signing secret (min 32 bytes) |
| OPENAI_API_KEY | yes | OpenAI API key for Agents SDK |
| ACCESS_TOKEN_EXPIRE_MINUTES | no | JWT TTL, default 1440 |
| RATE_LIMIT_DEFAULT | no | Rate limit rule, default 5/minute |

### Frontend (.env.local)

| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL_NEON | yes | Neon PostgreSQL connection string |
| BETTER_AUTH_SECRET | yes | Same secret as backend |
| NEXT_PUBLIC_API_URL | yes | Backend API base URL |

## Validation Checklist

- [ ] Backend starts without errors on port 8000
- [ ] Frontend starts without errors on port 3000
- [ ] User can sign up and sign in
- [ ] Chat interface loads after authentication
- [ ] "Add a task" creates a task via chat
- [ ] "Show my tasks" lists tasks via chat
- [ ] "Complete task" marks task as done via chat
- [ ] Conversation history persists after page refresh
- [ ] Server restart does not lose any data
