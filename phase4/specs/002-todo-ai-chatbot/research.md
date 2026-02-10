# Research: Todo AI Chatbot

**Branch**: `002-todo-ai-chatbot` | **Date**: 2026-02-08

## Existing Codebase Analysis

### Frontend (Phase 3)

**Framework**: Next.js 14.2.21 + React 18.3.1 + TypeScript 5.7.3
**Styling**: TailwindCSS 3.4.17 with custom CSS animations
**Auth**: Better Auth 1.4.10 (client + server)
**Database**: Drizzle ORM 0.41.0 + Neon Serverless 0.10.4
**Current State**: Task management dashboard with auth UI. No chat
interface exists yet.

**Existing Components** (7 total):
- `AuthForm.tsx` — unified sign in/up with Better Auth
- `TaskForm.tsx` — task creation modal with staggered animations
- `TaskList.tsx` — grid display with filters and progress bar
- `TaskItem.tsx` — individual task card
- `Navbar.tsx` — navigation header
- `RecurrenceSelector.tsx` — recurring task pattern UI
- `ReminderToggle.tsx` — reminder offset configuration

**Animation System** (globals.css, 338 lines):
- 10 keyframe animations (fadeInUp, scaleIn, shimmer, pulse-glow, etc.)
- Stagger classes (stagger-1 through stagger-6)
- Glassmorphism effects (.glass, .glass-strong)
- Gradient meshes (dark theme: purple/pink/cyan)
- Button/input/badge component styles

**Database Schema** (Drizzle/frontend):
- `user` — Better Auth managed (id, name, email, emailVerified, image)
- `session` — Better Auth sessions (token, expiresAt, userId)
- `account` — Better Auth accounts (OAuth/credential providers)
- `verification` — Better Auth email verification
- `task` — Application tasks (userId, title, description, completed,
  priority, dueDate, recurrencePattern, reminderEnabled, etc.)

### Backend (Phase 3)

**Framework**: FastAPI 0.104.1 + Python
**ORM**: SQLModel (SQLAlchemy + Pydantic)
**Database**: Neon PostgreSQL via asyncpg 0.31.0
**Auth**: JWT (python-jose 3.3.0) + bcrypt 4.1.2
**Rate Limiting**: slowapi 0.1.9

**Existing Structure**:
```
backend/src/
├── main.py              # FastAPI app, routers, exception handlers
├── config.py            # Pydantic settings (DB_URL, AUTH_SECRET)
├── database/
│   ├── database.py      # Async + sync engines (Neon PostgreSQL)
│   └── session.py       # Session dependency injection
├── models/
│   ├── user.py          # User SQLModel (id, email, name, hashed_password)
│   └── task.py          # Task SQLModel (id, user_id, title, desc, completed, priority, due_date)
├── routes/
│   ├── auth.py          # POST /api/signup, POST /api/signin
│   └── tasks.py         # CRUD: GET/POST/PUT/DELETE/PATCH /{user_id}/tasks
├── services/
│   ├── user_service.py  # Registration, authentication, JWT creation
│   └── task_service.py  # User-scoped CRUD operations
├── dependencies/
│   └── auth.py          # JWT extraction, user_id path verification
├── middleware/
│   ├── auth.py          # Auth middleware
│   └── rate_limit.py    # slowapi rate limiter setup
├── schemas/
│   ├── user.py          # Registration/login request/response
│   ├── responses.py     # BaseResponse, TokenResponse, ErrorResponse
│   └── errors.py        # ErrorDetail, ValidationErrorResponse
├── utils/
│   ├── jwt.py           # create_access_token, verify_token
│   ├── password.py      # hash_password, verify_password, validate_strength
│   └── validation.py    # Input validators
└── exceptions/
    └── handlers.py      # HTTP, validation, rate limit, general handlers
```

**API Endpoints** (existing):
- `POST /api/signup` — user registration (rate limited 5/min)
- `POST /api/signin` — user login (rate limited 5/min)
- `GET /{user_id}/tasks` — list tasks (JWT required)
- `POST /{user_id}/tasks` — create task (JWT required)
- `GET /{user_id}/tasks/{id}` — get task (JWT required)
- `PUT /{user_id}/tasks/{id}` — update task (JWT required)
- `DELETE /{user_id}/tasks/{id}` — delete task (JWT required)
- `PATCH /{user_id}/tasks/{id}/complete` — toggle completion (JWT required)

**Key Config** (.env):
- `DATABASE_URL` = Neon PostgreSQL (asyncpg driver)
- `BETTER_AUTH_SECRET` = JWT signing secret (shared with frontend)
- `ACCESS_TOKEN_EXPIRE_MINUTES` = 1440 (24 hours)

## Technology Research

### 1. OpenAI Agents SDK

**Decision**: Use `openai-agents` Python SDK for agent orchestration
**Rationale**: Official SDK provides agent creation, tool registration,
handoffs between agents, and built-in function calling. Aligns with
constitution requirement for multi-agent architecture.
**Alternatives considered**:
- LangChain — heavier, more abstraction than needed
- Raw OpenAI API — no agent orchestration primitives
- CrewAI — less mature, different paradigm

**Key concepts**:
- `Agent` class defines an agent with instructions and tools
- `Runner.run()` executes agent with conversation context
- Tools are Python functions decorated with `@function_tool`
- Handoffs route between agents (triage → specialist)
- `RunContext` provides shared state across tool calls

### 2. ChatKit UI Library

**Decision**: Use `@chatscope/chat-ui-kit-react` for chat components
**Rationale**: Most mature React chat UI kit with message lists,
input controls, typing indicators, and avatar support. Works with
Next.js App Router and supports custom styling.
**Alternatives considered**:
- Build custom chat UI — more effort, less polish
- `react-chat-elements` — less maintained, fewer features
- `stream-chat-react` — requires Stream service, overkill

**Key components**:
- `MainContainer`, `ChatContainer` — layout
- `MessageList`, `Message` — message display
- `MessageInput` — user input with send button
- `TypingIndicator` — loading state
- `Avatar` — user/bot avatars
- Custom CSS theming to match existing glassmorphism design

### 3. MCP Tool Architecture

**Decision**: Implement MCP tools as Python functions registered with
OpenAI Agents SDK's `@function_tool` decorator
**Rationale**: Each MCP tool maps directly to an existing service
method in the backend. The tools wrap the existing `TaskService` and
new service classes for reminders, tags, and analytics.
**Alternatives considered**:
- Separate MCP server process — unnecessary complexity for this scope
- Direct database calls in tools — violates service layer pattern

**Integration pattern**:
```
User message → FastAPI chat endpoint
  → OpenAI Agents SDK Runner
    → Triage Agent (routes to specialist)
      → Task/Reminder/Tag/Analytics Agent
        → MCP tool function
          → Service layer (existing)
            → Database (Neon PostgreSQL)
```

### 4. Conversation Persistence

**Decision**: Store conversation messages in a `conversation_message`
table in Neon PostgreSQL
**Rationale**: Constitution requires stateless server with DB-persisted
conversations. Each message stores role (user/assistant), content, and
timestamp linked to user_id.
**Alternatives considered**:
- Redis for conversation cache — adds infrastructure, not persistent
- File-based storage — not scalable, not cloud-native
- Frontend-only storage — violates statelessness requirement

### 5. Authentication Integration

**Decision**: Reuse existing Better Auth (frontend) + JWT (backend)
pattern for chat endpoint authentication
**Rationale**: The auth infrastructure already exists and works.
The chat endpoint `/api/{user_id}/chat` will use the same JWT Bearer
token verification as existing task endpoints.
**Alternatives considered**:
- WebSocket with token — adds complexity for Phase 3 scope
- Session cookies — already handled by Better Auth, JWT is simpler
  for API calls

### 6. Frontend-Backend Communication

**Decision**: HTTP POST for chat messages (not WebSocket)
**Rationale**: Each chat interaction is a request/response pair. The
stateless constitution requirement aligns with HTTP. WebSocket would
add streaming capability but is not required by the spec.
**Alternatives considered**:
- WebSocket — adds real-time but unnecessary complexity
- Server-Sent Events — good for streaming but spec doesn't require it
- HTTP + polling — wasteful, no advantage over direct POST
