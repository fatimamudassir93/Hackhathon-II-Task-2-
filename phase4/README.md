---
title: TODO App Backend
emoji: 📝
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# TODO App Backend API

FastAPI backend with AI chatbot for task management.

## Features
- Task CRUD operations
- AI chatbot with Groq LLM
- Better Auth integration
- PostgreSQL database

## Environment Variables Required

Set these in Hugging Face Space Settings:

```
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
BETTER_AUTH_SECRET=your-secret-key
GROQ_API_KEY=your-groq-api-key
LLM_PROVIDER=groq
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /docs` - API documentation
- `POST /api/tasks` - Create task
- `GET /api/tasks` - List tasks
- `POST /api/chat` - Chat with AI assistant
