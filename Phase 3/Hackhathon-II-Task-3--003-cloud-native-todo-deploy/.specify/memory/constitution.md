<!-- SYNC IMPACT REPORT
Version change: 2.0.0 → 3.0.0
Bump rationale: MAJOR — complete project scope change from full-stack
web app to AI chatbot with new technology bindings, agent architecture,
and MCP tool contracts. All principles redefined.

Modified principles:
- "Technology Binding Adherence" → "Technology Binding Adherence" (redefined)
- "Authentication Architecture Compliance" → "Authentication Architecture Compliance" (redefined for Better Auth)
- "Test-First (NON-NEGOTIABLE)" → "Test-First (NON-NEGOTIABLE)" (retained, updated scope)
- "REST API Contract Enforcement" → removed (replaced by MCP Tool Contract Enforcement)
- "Feature Scope Lock" → "Feature Scope Lock" (redefined for chatbot scope)
- "Spec-Driven Execution Compliance" → "Spec-Driven Execution Compliance" (retained)

Added sections:
- Agent Architecture Compliance (new principle)
- MCP Tool Contract Enforcement (replaces REST API)
- Conversation & Statelessness Rules (new principle)
- Agent definitions table
- MCP Tools inventory

Removed sections:
- REST API Contract Enforcement (replaced by MCP Tool Contract)
- Frontend and Backend Rules (replaced by agent-specific rules)

Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending (Constitution Check gates need refresh)
- .specify/templates/spec-template.md ✅ no structural changes needed
- .specify/templates/tasks-template.md ⚠ pending (task categories need agent phases)

Follow-up TODOs: None
-->

# Phase III – Todo AI Chatbot Constitution

## Core Principles

### I. Technology Binding Adherence

Frontend: ChatKit UI for conversational interface. Backend: Python
FastAPI with OpenAI Agents SDK for agent orchestration and MCP tool
execution. Database: Neon Serverless PostgreSQL for persistent task
storage, conversation history, and user-scoped data. Authentication:
Better Auth for user signup, signin, and session management.
Responsibilities MUST NOT cross layers — each technology has fixed
responsibilities that MUST NOT be mixed.

### II. Agent Architecture Compliance

The system MUST implement a multi-agent architecture with the
following agents:

| Agent | Purpose | Tools |
|-------|---------|-------|
| Task Agent | Task CRUD operations | add_task, list_tasks, update_task, complete_task, delete_task |
| Reminder Agent | Manage time-based reminders | schedule_reminder, cancel_reminder, list_reminders |
| User/Auth Agent | Authentication flows | signup, login, logout, password_reset |
| Tag/Category Agent | Organize and filter tasks | add_tag, remove_tag, list_tags, filter_tasks_by_tag |
| Analytics Agent | Task insights and metrics | count_tasks, tasks_done, tasks_pending |
| Integration Agent | Optional external sync | Calendar/Slack/Email sync |

Each agent MUST have a clearly defined scope. Agents MUST NOT
perform operations outside their designated tools. The OpenAI Agents
SDK MUST be used for agent orchestration, routing, and handoffs.

### III. Authentication Architecture Compliance

Authentication flow is fixed: User signs up/signs in via Better Auth.
Better Auth issues session tokens. Frontend attaches credentials to
every API and chat request. Backend verifies authentication before
routing to any agent. All MCP tool calls MUST include authenticated
user_id. Users MUST only access their own data — cross-user access
MUST be rejected.

### IV. MCP Tool Contract Enforcement

All task operations MUST be exposed as MCP tools, not raw REST
endpoints. The following MCP tools are the authoritative contract:

- `add_task(user_id, title, description)` → task_id, status
- `list_tasks(user_id, status)` → array of tasks
- `update_task(user_id, task_id, title, description)` → task_id, status
- `complete_task(user_id, task_id)` → task_id, status
- `delete_task(user_id, task_id)` → task_id, status
- `schedule_reminder(user_id, task_id, datetime)` → reminder_id, status
- `cancel_reminder(user_id, reminder_id)` → reminder_id, status
- `list_reminders(user_id)` → array of reminders
- `add_tag(user_id, task_id, tag)` → task_id, tags
- `remove_tag(user_id, task_id, tag)` → task_id, tags
- `list_tags(user_id)` → array of tags
- `filter_tasks_by_tag(user_id, tag)` → array of tasks

All tools MUST validate user_id ownership. Tools MUST return
structured responses. New tools MUST NOT be added without spec update.

### V. Test-First (NON-NEGOTIABLE)

TDD mandatory: Tests written, user approved, tests fail, then
implement. Red-Green-Refactor cycle strictly enforced. All MCP tools
MUST have unit tests for success and error paths. Agent routing MUST
be tested to verify correct tool dispatch. User isolation MUST be
tested to ensure users can only access their own data. Conversation
flow MUST be tested end-to-end.

### VI. Conversation & Statelessness Rules

The server MUST be stateless — all conversation context MUST be
persisted in the database. Natural language input MUST be mapped to
MCP tool calls by the appropriate agent. The system MUST confirm
actions back to the user after execution. Errors MUST be surfaced as
user-friendly messages in the chat. Conversation history MUST be
stored per-user in Neon PostgreSQL.

### VII. Feature Scope Lock

Implementation restricted to:
- Natural language task management (add, delete, update, view, complete)
- Reminder scheduling and management
- Tag/category organization and filtering
- Task analytics (count, done, pending)
- User signup/signin via Better Auth
- Conversation persistence in database

Optional (requires explicit approval):
- Integration Agent (Calendar/Slack/Email sync)

Prohibited features: Kubernetes/Docker orchestration, Kafka/Dapr
event streaming, background job queues, voice input, multilingual
support, file uploads. No scope creep allowed without explicit spec
update.

### VIII. Spec-Driven Execution Compliance

MUST read specs before implementation, reference specs explicitly.
If requirement is missing or unclear, STOP and request spec update.
Do NOT invent agent behavior, MCP tool signatures, database fields,
or UI flows. Specs and this constitution are the single source of
truth. Agent definitions and MCP tool contracts in `/specs` are
authoritative.

## Frontend Rules (ChatKit UI)

Use ChatKit UI components for the conversational interface. Chat
messages MUST be rendered with proper formatting (markdown, lists).
Authentication UI (signup/signin) handled by Better Auth integration.
Loading states MUST be shown during agent processing. Error states
MUST be displayed inline in the chat. The frontend MUST NOT call MCP
tools directly — all interactions go through the chat API.

## Backend Rules (FastAPI + OpenAI Agents SDK)

Use FastAPI for HTTP layer and WebSocket support. Use OpenAI Agents
SDK for agent orchestration and MCP tool dispatch. All MCP tools MUST
validate inputs and return structured JSON responses. Agent routing
MUST map user intent to the correct agent. Backend operates in
Zero-Trust mode — never trust frontend input. All database operations
MUST go through SQLModel or equivalent ORM. Conversation history MUST
be persisted after each exchange.

## Quality Gates (Mandatory)

Before completion, verify:
- Agent routing correctly dispatches to the right agent for each intent
- All MCP tools enforce user_id ownership
- Conversation state is persisted and recoverable
- Better Auth authentication is enforced on all chat endpoints
- Users can access ONLY their own tasks, reminders, and tags
- ChatKit UI renders messages correctly with loading/error states
- Server is stateless — restart does not lose conversation history

Failure at any gate invalidates the implementation and requires
spec refinement.

## Governance

This constitution supersedes all other practices for Phase III. All
chat endpoints MUST require authentication via Better Auth. All MCP
tools MUST enforce user ownership. Code reviews MUST verify compliance
with agent architecture and MCP tool contracts. Complexity MUST be
justified with explicit reference to this constitution. Use Spec-Kit
Plus for runtime development guidance.

**Version**: 3.0.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-02-08
