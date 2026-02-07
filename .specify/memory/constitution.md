<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 2.0.0
Modified principles: All principles updated to reflect Phase II Todo application requirements
Added sections: Authentication Architecture, REST API Contract, Feature Scope Lock, Spec-Driven Execution Rules
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ✅ updated
Follow-up TODOs: None
-->

# Phase II – Todo Full-Stack Web Application Constitution

## Core Principles

### I. Technology Binding Adherence
Frontend: Next.js 16+ (App Router) with TypeScript, using Better Auth for authentication. Backend: Python FastAPI for REST API implementation, JWT verification, and authorization. ORM: SQLModel for database models, queries, and logical migrations. Database: Neon Serverless PostgreSQL for persistent task storage and user-scoped data. Responsibilities must NOT cross layers - each technology has fixed responsibilities that cannot be mixed.

### II. Authentication Architecture Compliance
Authentication flow is fixed: User signs up/signs in via Better Auth (Next.js frontend), which issues a JWT token. Frontend attaches token to every API request as Authorization: Bearer <JWT>. FastAPI backend extracts token, verifies using shared BETTER_AUTH_SECRET, decodes user_id, compares JWT user_id with URL user_id, and filters all data by authenticated user_id. Both frontend and backend must use the same secret.

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced. All API endpoints must have authentication and authorization tests. User isolation must be tested to ensure users can only access their own tasks. All CRUD operations require comprehensive test coverage.

### IV. REST API Contract Enforcement
All API routes must live under /api, require JWT authentication, and enforce user ownership. Authorized endpoints: GET /api/{user_id}/tasks, POST /api/{user_id}/tasks, GET /api/{user_id}/tasks/{id}, PUT /api/{user_id}/tasks/{id}, DELETE /api/{user_id}/tasks/{id}, PATCH /api/{user_id}/tasks/{id}/complete. Requests without valid JWT → 401 Unauthorized. Cross-user access → 403 Forbidden.

### V. Feature Scope Lock
Implementation restricted to: Add task, Delete task, Update task, View task list, Mark task complete, User signup/signin, Persistent storage. Prohibited features: Chatbot, AI agents, Kubernetes/Docker, Kafka/Dapr, Background jobs, Voice or multilingual features. No scope creep allowed without explicit spec update.

### VI. Spec-Driven Execution Compliance
Must read specs before implementation, reference specs explicitly (@specs/features/..., @specs/api/..., @specs/database/..., @specs/ui/...). If requirement is missing or unclear, STOP and request spec update. Do NOT invent API behavior, database fields, or UI flows. Specs are the single source of truth.

## Frontend and Backend Rules

### Frontend Rules (Next.js)
Use Server Components by default, Client Components only for interactivity. All API calls go through a single API client module. JWT must be attached automatically. UI must show loading states, error states, and empty states. Authentication UI (signup/signin) handled by Better Auth.

### Backend Rules (FastAPI)
Use FastAPI + SQLModel only, no raw SQL unless specified. Validate all inputs, handle all errors with JSON responses. Never trust frontend input blindly. Backend operates in Zero-Trust mode. Must implement JWT verification and authorization checks on all endpoints.

## Quality Gates (Mandatory)

Before completion, verify: Tech responsibilities were not mixed, JWT auth is enforced on all endpoints, users can access ONLY their own tasks, Folder structure matches monorepo spec, App runs locally as documented. Failure → implementation invalid → regenerate via spec refinement.

## Governance

Constitution supersedes all other practices. All API endpoints must require JWT authentication and enforce user ownership. Code reviews must verify compliance with authentication architecture and API contract. Complexity must be justified with explicit reference to this constitution. Use Spec-Kit Plus for runtime development guidance.

**Version**: 2.0.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-09