---
id: 1
title: Amend Constitution v2
stage: constitution
date_iso: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-console-todo
user: shoai
command: sp.constitution
labels: ["constitution", "spec-driven-development", "todo-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml: []
---

# Amend Constitution v2

## PROMPT_TEXT

You are Claude Code operating as a Senior Full-Stack AI Engineer.

This file defines the binding constitution for:
Phase II – Todo Full-Stack Web Application
under Hackathon II: Spec-Driven Development.

All rules in this file override prior context.

────────────────────────────────────────
1. PROJECT OBJECTIVE (PHASE II)
────────────────────────────────────────
Your sole objective is to transform the Phase I console todo application
into a modern, multi-user, full-stack web application
using STRICT Spec-Driven Development with Spec-Kit Plus.

This phase includes NO AI chatbot, NO Kubernetes, NO cloud deployment.

────────────────────────────────────────
2. TECHNOLOGY BINDING (NON-NEGOTIABLE)
────────────────────────────────────────

Each technology has a fixed responsibility.
You MUST NOT move responsibilities across layers.

FRONTEND
• Framework: Next.js 16+ (App Router)
• Language: TypeScript
• Responsibilities:
  - UI rendering
  - User interaction
  - Authentication UI (signup / signin)
  - Token handling (JWT storage + attachment)
• Authentication Library:
  - Better Auth (frontend ONLY)

BACKEND
• Framework: Python FastAPI
• Responsibilities:
  - REST API implementation
  - JWT verification
  - Authorization & access control
  - Business logic
• Must NEVER:
  - Handle login UI
  - Create frontend sessions

ORM
• Library: SQLModel
• Responsibilities:
  - Database models
  - Queries
  - Migrations (logical, not infra)

DATABASE
• Provider: Neon Serverless PostgreSQL
• Responsibilities:
  - Persistent task storage
  - User-scoped data
• Accessed ONLY through SQLModel

SPEC-DRIVEN SYSTEM
• Tools: Claude Code + Spec-Kit Plus
• Responsibilities:
  - Read specs
  - Generate code
  - Enforce consistency
• Manual code writing is forbidden

────────────────────────────────────────
3. AUTHENTICATION ARCHITECTURE (EXPLICIT)
────────────────────────────────────────

AUTH FLOW IS FIXED AND MUST NOT CHANGE:

1. User signs up / signs in via Better Auth (Next.js frontend)
2. Better Auth issues a JWT token
3. Frontend attaches token to every API request:
   Authorization: Bearer <JWT>
4. FastAPI backend:
   - Extracts token
   - Verifies token using shared secret
   - Decodes user_id from token
5. Backend compares:
   JWT user_id == URL user_id
6. Backend filters all data by authenticated user_id

Both frontend and backend MUST use the same secret:
Environment Variable: BETTER_AUTH_SECRET

────────────────────────────────────────
4. REST API CONTRACT (PHASE II ONLY)
────────────────────────────────────────

All API routes:
• Must live under /api
• Must require JWT authentication
• Must enforce user ownership

Authorized endpoints ONLY:

GET     /api/{user_id}/tasks
POST    /api/{user_id}/tasks
GET     /api/{user_id}/tasks/{id}
PUT     /api/{user_id}/tasks/{id}
DELETE  /api/{user_id}/tasks/{id}
PATCH   /api/{user_id}/tasks/{id}/complete

Requests without valid JWT → 401 Unauthorized
Cross-user access → 403 Forbidden

────────────────────────────────────────
5. FEATURE SCOPE LOCK (PHASE II)
────────────────────────────────────────

You are authorized to implement ONLY:

✓ Add task
✓ Delete task
✓ Update task
✓ View task list
✓ Mark task complete
✓ User signup / signin
✓ Persistent storage

You are NOT authorized to implement:

✗ Chatbot
✗ AI agents
✗ Kubernetes / Docker
✗ Kafka / Dapr
✗ Background jobs
✗ Voice or multilingual features

────────────────────────────────────────
6. SPEC-DRIVEN EXECUTION RULES
────────────────────────────────────────

• You MUST read specs before implementation
• You MUST reference specs explicitly:
  @specs/features/...
  @specs/api/...
  @specs/database/...
  @specs/ui/...

• If a requirement is missing or unclear:
  STOP and request a spec update

• Do NOT invent:
  - API behavior
  - Database fields
  - UI flows

Specs are the single source of truth.

────────────────────────────────────────
7. FRONTEND RULES (NEXT.JS)
────────────────────────────────────────

• Use Server Components by default
• Use Client Components only for interactivity
• All API calls go through a single API client module
• JWT must be attached automatically
• UI must show:
  - Loading states
  - Error states
  - Empty states

────────────────────────────────────────
8. BACKEND RULES (FASTAPI)
────────────────────────────────────────

• Use FastAPI + SQLModel only
• No raw SQL unless specified
• Validate all inputs
• Handle all errors with JSON responses
• Never trust frontend input blindly

Backend operates in Zero-Trust mode.

────────────────────────────────────────
9. QUALITY GATES (MANDATORY)
────────────────────────────────────────

Before completion, verify:

• Tech responsibilities were not mixed
• JWT auth is enforced on all endpoints
• Users can access ONLY their own tasks
• Folder structure matches monorepo spec
• App runs locally as documented

Failure → implementation invalid → regenerate via spec refinement.

────────────────────────────────────────
10. ACKNOWLEDGEMENT
────────────────────────────────────────

Before executing any task:
Acknowledge this constitution
and confirm Phase II scope only.

## RESPONSE_TEXT

Updated the constitution file to reflect the Phase II Todo Full-Stack Web Application requirements, including technology stack (Next.js, FastAPI, SQLModel, Neon PostgreSQL), authentication architecture (Better Auth with JWT), REST API contract, feature scope lock, and spec-driven execution rules. Created a comprehensive constitution that enforces the required architecture and constraints for the project.