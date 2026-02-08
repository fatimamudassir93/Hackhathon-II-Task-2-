# TODO App Architecture

## System Overview

The TODO application is a cloud-native, full-stack web application with AI-powered chatbot capabilities for natural language task management.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│                    (Web Interface)                           │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Vercel Edge Network                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           Next.js Frontend (SSR + CSR)                │  │
│  │  - React Components                                   │  │
│  │  - Better Auth Client                                 │  │
│  │  - Chat Interface                                     │  │
│  │  - Task Management UI                                 │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Railway Platform                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              FastAPI Backend                          │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │         Core API Layer                          │ │  │
│  │  │  - Task CRUD Endpoints                          │ │  │
│  │  │  - Authentication (Better Auth)                 │ │  │
│  │  │  - Rate Limiting                                │ │  │
│  │  │  - CORS Middleware                              │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │         AI Chatbot System                       │ │  │
│  │  │  - Multi-Agent Architecture                     │ │  │
│  │  │  - Task Agent (CRUD operations)                 │ │  │
│  │  │  - Tag Agent (tag management)                   │ │  │
│  │  │  - Reminder Agent (scheduling)                  │ │  │
│  │  │  - Analytics Agent (statistics)                 │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │         LLM Integration Layer                   │ │  │
│  │  │  - OpenAI Provider                              │ │  │
│  │  │  - Groq Provider                                │ │  │
│  │  │  - Gemini Provider                              │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ PostgreSQL Protocol (SSL)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Neon PostgreSQL                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Database Schema                          │  │
│  │  - users (Better Auth managed)                        │  │
│  │  - sessions (Better Auth managed)                     │  │
│  │  - tasks (user tasks)                                 │  │
│  │  - tags (task tags)                                   │  │
│  │  - task_tags (many-to-many)                           │  │
│  │  - reminders (scheduled reminders)                    │  │
│  │  - conversation_messages (chat history)               │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

External Services:
┌──────────────┐
│ LLM Providers│
│ - OpenAI     │
│ - Groq       │
│ - Gemini     │
└──────────────┘
```

## Technology Stack

### Frontend (Vercel)
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **UI Library**: React 18
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth (client-side)
- **State Management**: React Hooks
- **HTTP Client**: Fetch API
- **Deployment**: Vercel (Edge Network)

### Backend (Railway)
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLModel
- **Authentication**: Better Auth (JWT)
- **Rate Limiting**: slowapi
- **CORS**: FastAPI middleware
- **Validation**: Pydantic
- **Deployment**: Railway (Docker container)

### Database (Neon)
- **Database**: PostgreSQL 15+
- **Hosting**: Neon Serverless
- **Connection**: SSL/TLS encrypted
- **Pooling**: Built-in connection pooling

### AI/LLM
- **Providers**: OpenAI, Groq, Gemini
- **Architecture**: Multi-agent system
- **Tools**: 15 specialized tools
- **Agents**: 4 domain-specific agents

## Component Architecture

### Frontend Components

```
app/
├── (auth)/
│   ├── sign-in/          # Authentication pages
│   └── sign-up/
├── api/
│   ├── auth/             # Better Auth API routes
│   └── tasks/            # Task proxy routes
├── dashboard/            # Main dashboard
├── chat/                 # Chat interface
└── layout.tsx            # Root layout

components/
├── ChatInterface.tsx     # Main chat component
├── ChatMessage.tsx       # Message display
├── ToolCallDisplay.tsx   # Tool execution display
├── TaskList.tsx          # Task list component
└── TaskItem.tsx          # Individual task

lib/
├── auth.ts               # Better Auth config
├── auth-client.ts        # Client auth utilities
├── db.ts                 # Database connection
├── schema.ts             # Drizzle schema
└── chat-api.ts           # Chat API client
```

### Backend Components

```
backend/
├── src/
│   ├── main.py           # FastAPI app entry
│   ├── routes/
│   │   └── tasks.py      # Task CRUD endpoints
│   ├── models/
│   │   ├── task.py       # Task model
│   │   ├── tag.py        # Tag models
│   │   └── reminder.py   # Reminder model
│   ├── services/
│   │   └── task_service.py
│   ├── middleware/
│   │   └── rate_limit.py
│   └── database/
│       └── database.py   # DB connection
│
└── chatbot/
    ├── routes/
    │   └── chat.py       # Chat endpoints
    ├── agents/
    │   ├── task_agent.py
    │   ├── tag_agent.py
    │   ├── reminder_agent.py
    │   └── analytics_agent.py
    ├── llm/
    │   ├── openai_provider.py
    │   ├── groq_provider.py
    │   └── gemini_provider.py
    ├── tools/            # 15 specialized tools
    └── models/
        └── conversation.py
```

## Data Flow

### Task Creation Flow

```
1. User enters task in UI
   ↓
2. Frontend sends POST /api/tasks
   ↓
3. Backend validates request
   ↓
4. Backend checks authentication
   ↓
5. Backend creates task in database
   ↓
6. Backend returns task object
   ↓
7. Frontend updates UI
```

### Chat Interaction Flow

```
1. User sends message in chat
   ↓
2. Frontend sends POST /api/{user_id}/chat
   ↓
3. Backend receives message
   ↓
4. Chatbot router selects appropriate agent
   ↓
5. Agent processes message with LLM
   ↓
6. LLM determines required tools
   ↓
7. Agent executes tools (e.g., create task)
   ↓
8. Agent formats response
   ↓
9. Backend returns response
   ↓
10. Frontend displays message and tool results
```

## Security Architecture

### Authentication Flow

```
1. User signs up/in via Better Auth
   ↓
2. Better Auth creates session
   ↓
3. JWT token issued
   ↓
4. Token stored in httpOnly cookie
   ↓
5. Frontend includes token in requests
   ↓
6. Backend validates token
   ↓
7. Backend extracts user ID
   ↓
8. Backend filters data by user ID
```

### Security Layers

1. **Transport Security**: HTTPS everywhere
2. **Authentication**: JWT tokens with Better Auth
3. **Authorization**: User-based data isolation
4. **Rate Limiting**: Per-endpoint rate limits
5. **CORS**: Restricted to frontend domain
6. **Input Validation**: Pydantic models
7. **SQL Injection Prevention**: ORM (SQLModel)
8. **XSS Prevention**: React auto-escaping

## Deployment Architecture

### CI/CD Pipeline

```
Developer pushes code
   ↓
GitHub receives push
   ↓
┌─────────────────┬─────────────────┐
│                 │                 │
│  Backend Path   │  Frontend Path  │
│                 │                 │
│  GitHub Actions │  Vercel Auto    │
│  - Run tests    │  - Build        │
│  - Build Docker │  - Deploy       │
│  - Deploy       │  - Activate     │
│    to Railway   │                 │
│                 │                 │
└─────────────────┴─────────────────┘
   ↓                 ↓
Railway            Vercel
Production         Production
```

### Scaling Strategy

**Frontend (Vercel)**:
- Edge network (automatic global distribution)
- Automatic scaling
- CDN for static assets
- Serverless functions for API routes

**Backend (Railway)**:
- Horizontal scaling (manual/automatic)
- Container-based deployment
- Health checks and auto-restart
- Rolling deployments

**Database (Neon)**:
- Serverless PostgreSQL
- Automatic scaling
- Connection pooling
- Read replicas (if needed)

## Performance Characteristics

### Response Times (Target)
- **Static Pages**: < 100ms (CDN)
- **API Endpoints**: < 200ms (p95)
- **Chat Responses**: 1-3s (LLM dependent)
- **Database Queries**: < 50ms (p95)

### Throughput
- **Frontend**: Unlimited (Vercel edge)
- **Backend**: ~1000 req/min (single instance)
- **Database**: ~100 concurrent connections

## Monitoring & Observability

### Metrics Collected
- **Frontend**: Web Vitals, page load times, errors
- **Backend**: Request rate, response time, error rate
- **Database**: Connection count, query performance

### Logging
- **Frontend**: Vercel logs (errors, warnings)
- **Backend**: Railway logs (structured JSON)
- **Database**: Neon query logs

## Disaster Recovery

### Backup Strategy
- **Database**: Neon automatic backups (point-in-time recovery)
- **Code**: Git repository (GitHub)
- **Configuration**: Environment variables documented

### Rollback Procedure
- **Frontend**: Instant rollback via Vercel dashboard
- **Backend**: Redeploy previous version via Railway
- **Database**: Point-in-time recovery via Neon

## Cost Structure

### Monthly Costs (Estimated)
- **Vercel**: $0 (Hobby tier)
- **Railway**: $5-10 (free tier + usage)
- **Neon**: $0 (free tier)
- **LLM API**: Variable (pay-per-use)
- **Total**: $5-10/month + LLM usage

## Future Enhancements

### Planned Improvements
1. **Caching**: Redis for session/response caching
2. **CDN**: CloudFlare for additional caching
3. **Monitoring**: Sentry for error tracking
4. **Analytics**: PostHog for user analytics
5. **Search**: Elasticsearch for full-text search
6. **Queue**: Background job processing
7. **WebSockets**: Real-time updates
8. **Mobile**: React Native mobile app

## References

- [Deployment Guide](./DEPLOYMENT.md)
- [Troubleshooting Guide](./TROUBLESHOOTING.md)
- [Runbook](./RUNBOOK.md)
