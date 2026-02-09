# Implementation Plan: Todo AI Chatbot

**Branch**: `002-todo-ai-chatbot` | **Date**: 2026-02-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-todo-ai-chatbot/spec.md`

## Summary

Build an AI chatbot that manages todos via natural language. The
system extends the existing FastAPI backend with OpenAI Agents SDK
for multi-agent orchestration and MCP tool execution, adds a ChatKit
UI chat interface to the Next.js frontend, and persists all
conversation history in Neon PostgreSQL. Six agents (Task, Reminder,
Tag, Analytics, Auth, Integration) route user intent to 15 MCP tools.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.7 (frontend)
**Primary Dependencies**:
- Backend: FastAPI 0.104.1, OpenAI Agents SDK (`openai-agents`),
  SQLModel, asyncpg 0.31.0
- Frontend: Next.js 14.2, React 18.3, `@chatscope/chat-ui-kit-react`,
  Better Auth 1.4.10, Drizzle ORM 0.41.0
**Storage**: Neon Serverless PostgreSQL (existing, shared by frontend
and backend)
**Testing**: pytest + httpx (backend), Jest/React Testing Library
(frontend)
**Target Platform**: Web application (desktop + mobile browser)
**Project Type**: Web (frontend + backend monorepo)
**Performance Goals**: <5s per chat response, 100 concurrent users
**Constraints**: Stateless server, all state in DB, HTTP POST for
chat (no WebSocket)
**Scale/Scope**: Single-tenant per user, ~6 agents, 15 MCP tools

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Technology Binding | PASS | ChatKit UI (frontend), FastAPI + OpenAI Agents SDK (backend), Neon PostgreSQL (DB), Better Auth (auth) |
| II. Agent Architecture | PASS | 6 agents defined with scoped tools per constitution table |
| III. Auth Architecture | PASS | Better Auth (frontend) + JWT (backend), user_id in all MCP tools |
| IV. MCP Tool Contract | PASS | 15 tools defined in contracts/mcp-tools.md matching constitution |
| V. Test-First | PASS | Plan includes test phases before implementation |
| VI. Conversation & Statelessness | PASS | conversation_message table, stateless server design |
| VII. Feature Scope Lock | PASS | Only specified features, Integration Agent marked optional |
| VIII. Spec-Driven Execution | PASS | All implementation references spec and contracts |

## Codebase Analysis

### Existing Backend Assets (Reusable)

The current backend provides a solid foundation. The following
components are **directly reusable** for the chatbot:

| Component | Path | Reuse Strategy |
|-----------|------|----------------|
| FastAPI app setup | `backend/src/main.py` | Extend with chat router |
| Database engines | `backend/src/database/database.py` | Reuse async/sync engines |
| Session DI | `backend/src/database/session.py` | Reuse for new services |
| User model | `backend/src/models/user.py` | Reuse as-is |
| Task model | `backend/src/models/task.py` | Reuse, MCP tools wrap TaskService |
| TaskService | `backend/src/services/task_service.py` | MCP tools call this directly |
| UserService | `backend/src/services/user_service.py` | Reuse for auth |
| JWT auth | `backend/src/dependencies/auth.py` | Reuse for chat endpoint |
| Exception handlers | `backend/src/exceptions/handlers.py` | Reuse as-is |
| Rate limiter | `backend/src/middleware/rate_limit.py` | Apply to chat endpoint |
| Config/Settings | `backend/src/config.py` | Extend with OPENAI_API_KEY |

**New backend code needed**:
- `backend/src/agents/` — Agent definitions (triage + 5 specialists)
- `backend/src/tools/` — MCP tool functions (wrappers around services)
- `backend/src/models/tag.py` — Tag + TaskTag models
- `backend/src/models/reminder.py` — Reminder model
- `backend/src/models/conversation.py` — ConversationMessage model
- `backend/src/services/tag_service.py` — Tag CRUD service
- `backend/src/services/reminder_service.py` — Reminder CRUD service
- `backend/src/services/conversation_service.py` — Message persistence
- `backend/src/services/chat_service.py` — Orchestrates agent execution
- `backend/src/routes/chat.py` — POST /api/{user_id}/chat + GET history

### Existing Frontend Assets (Reusable)

| Component | Path | Reuse Strategy |
|-----------|------|----------------|
| Better Auth setup | `frontend/lib/auth.ts`, `auth-client.ts` | Reuse as-is |
| Database client | `frontend/lib/db.ts` | Reuse for conversation queries |
| Schema definitions | `frontend/lib/schema.ts` | Extend with conversation table |
| Auth UI | `frontend/components/AuthForm.tsx` | Reuse as-is |
| Navbar | `frontend/components/Navbar.tsx` | Extend with chat nav link |
| Animation system | `frontend/app/globals.css` | Extend with chat animations |
| Layout | `frontend/app/layout.tsx` | Reuse as-is |

**New frontend code needed**:
- `frontend/app/chat/page.tsx` — Chat page (main chat interface)
- `frontend/components/ChatInterface.tsx` — ChatKit container
- `frontend/components/ChatMessage.tsx` — Individual message rendering
- `frontend/components/ToolCallDisplay.tsx` — MCP tool call visualization
- `frontend/lib/chat-api.ts` — Chat API client (POST message, GET history)

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-ai-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   ├── chat-api.md      # Chat endpoint contract
│   └── mcp-tools.md     # MCP tool signatures
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py                    # Extend: add chat router
│   ├── config.py                  # Extend: add OPENAI_API_KEY
│   ├── agents/                    # NEW: Agent definitions
│   │   ├── __init__.py
│   │   ├── triage.py              # Triage agent (routes to specialists)
│   │   ├── task_agent.py          # Task CRUD agent
│   │   ├── reminder_agent.py      # Reminder management agent
│   │   ├── tag_agent.py           # Tag/category agent
│   │   └── analytics_agent.py     # Analytics agent
│   ├── tools/                     # NEW: MCP tool functions
│   │   ├── __init__.py
│   │   ├── task_tools.py          # add_task, list_tasks, etc.
│   │   ├── reminder_tools.py      # schedule_reminder, etc.
│   │   ├── tag_tools.py           # add_tag, remove_tag, etc.
│   │   └── analytics_tools.py     # count_tasks, tasks_done, etc.
│   ├── models/
│   │   ├── user.py                # Existing
│   │   ├── task.py                # Existing
│   │   ├── tag.py                 # NEW: Tag + TaskTag models
│   │   ├── reminder.py            # NEW: Reminder model
│   │   └── conversation.py        # NEW: ConversationMessage model
│   ├── services/
│   │   ├── user_service.py        # Existing
│   │   ├── task_service.py        # Existing
│   │   ├── tag_service.py         # NEW: Tag CRUD
│   │   ├── reminder_service.py    # NEW: Reminder CRUD
│   │   ├── conversation_service.py # NEW: Message persistence
│   │   └── chat_service.py        # NEW: Agent orchestration
│   ├── routes/
│   │   ├── auth.py                # Existing
│   │   ├── tasks.py               # Existing
│   │   └── chat.py                # NEW: Chat endpoint
│   └── ... (existing dirs unchanged)
└── tests/
    ├── test_tools/                # NEW: MCP tool tests
    │   ├── test_task_tools.py
    │   ├── test_reminder_tools.py
    │   ├── test_tag_tools.py
    │   └── test_analytics_tools.py
    ├── test_agents/               # NEW: Agent routing tests
    │   └── test_triage.py
    ├── test_services/             # NEW: Service tests
    │   ├── test_tag_service.py
    │   ├── test_reminder_service.py
    │   └── test_conversation_service.py
    └── test_routes/               # NEW: Chat endpoint tests
        └── test_chat.py

frontend/
├── app/
│   ├── chat/
│   │   └── page.tsx               # NEW: Chat page
│   └── ... (existing pages unchanged)
├── components/
│   ├── ChatInterface.tsx          # NEW: ChatKit container
│   ├── ChatMessage.tsx            # NEW: Message rendering
│   ├── ToolCallDisplay.tsx        # NEW: Tool call visualization
│   └── ... (existing components unchanged)
├── lib/
│   ├── chat-api.ts                # NEW: Chat API client
│   ├── schema.ts                  # Extend: conversation_message table
│   └── ... (existing libs unchanged)
└── ... (existing config unchanged)
```

**Structure Decision**: Web application pattern (frontend + backend)
extending the existing monorepo. New code is additive — no existing
files are deleted or restructured.

## Complexity Tracking

> No constitution violations found. All additions are within scope.

| Addition | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|-------------------------------------|
| Triage agent | Routes user intent to correct specialist agent | Single mega-agent would violate principle II (agent scope separation) |
| 3 new DB models (Tag, Reminder, Conversation) | Required by spec for tags, reminders, and chat persistence | Using existing task table for everything would violate data model clarity |
| ChatKit UI library | Required by constitution for conversational interface | Custom chat UI would take significantly more effort for less polish |

## Architecture Decisions

### Agent Routing Pattern

```
User message
  │
  ▼
POST /api/{user_id}/chat
  │
  ▼
JWT Auth Check (existing dependency)
  │
  ▼
ChatService.process_message()
  │
  ▼
Save user message to conversation_message table
  │
  ▼
Load conversation history (last N messages for context)
  │
  ▼
Triage Agent (OpenAI Agents SDK Runner.run())
  │ ── analyzes intent
  │ ── hands off to specialist agent
  │
  ├──→ Task Agent ──→ task_tools.py ──→ TaskService (existing)
  ├──→ Reminder Agent ──→ reminder_tools.py ──→ ReminderService (new)
  ├──→ Tag Agent ──→ tag_tools.py ──→ TagService (new)
  ├──→ Analytics Agent ──→ analytics_tools.py ──→ TaskService (existing)
  │
  ▼
Save assistant response + tool_calls to conversation_message table
  │
  ▼
Return {reply, tool_calls} to frontend
```

### Database Session Sharing

MCP tools need database access. The pattern is:
1. Chat endpoint creates an async database session
2. Session is stored in `RunContext` (OpenAI Agents SDK context)
3. Each MCP tool function receives context and uses the session
4. Transaction commits after all tools in a turn complete

### Frontend Chat Flow

```
User types message in ChatKit MessageInput
  │
  ▼
POST /api/{user_id}/chat with JWT Bearer token
  │
  ▼
Show TypingIndicator while waiting
  │
  ▼
Receive response {reply, tool_calls}
  │
  ▼
Render assistant message with ChatMessage component
  │ ── if tool_calls present, render ToolCallDisplay
  │
  ▼
Append to local message list
  │
  ▼
On page load: GET /api/{user_id}/chat/history to restore
```
