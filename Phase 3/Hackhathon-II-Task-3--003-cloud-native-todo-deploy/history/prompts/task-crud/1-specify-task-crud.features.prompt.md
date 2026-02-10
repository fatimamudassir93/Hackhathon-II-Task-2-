---
id: 1
title: Specify Task CRUD features
stage: spec
date_iso: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: task-crud
branch: 001-console-todo
user: shoai
command: sp.specify
labels: ["spec", "crud", "tasks", "api", "database"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/task-crud/spec.md
  - specs/api/rest-endpoints.md
  - specs/database/schema.md
  - specs/task-crud/checklists/requirements.md
tests_yaml: []
---

# Specify Task CRUD features

## PROMPT_TEXT

specify phase II task CRUD features You are Claude Code operating under /sp.constitute.

Your task is to SPECIFY the Task CRUD features for
Phase II – Todo Full-Stack Web Application
using Spec-Kit Plus conventions.

──────────────────────────────
1. SCOPE
──────────────────────────────
Include only the following features:

• Create Task
• View Tasks (list)
• Update Task
• Delete Task
• Toggle Completion

Do NOT include:
✗ Authentication (handled separately)
✗ AI chatbot
✗ Phase III+ features (recurring tasks, reminders, voice, multilingual)
✗ Cloud deployment

──────────────────────────────
2. SPEC FORMAT
──────────────────────────────
For each feature, generate or update:

1. Feature Specification
   → /specs/features/task-crud.md
   • Feature name
   • Phase: II
   • User stories
   • Acceptance criteria
   • Validation rules
   • Error cases
   • Authorization rules (user-specific)
   • References to API and database specs

2. API Specification
   → /specs/api/rest-endpoints.md
   • HTTP method
   • Full path (with /api/{user_id})
   • Required headers (Authorization: Bearer <JWT>)
   • Request body schema
   • Response schema
   • Error responses (401, 403, 404, 422)
   • Ownership enforcement

3. Database Specification
   → /specs/database/schema.md
   • Tables and columns
   • Types
   • Primary keys
   • Foreign keys
   • Indexes
   • Ownership constraints (user_id)

──────────────────────────────
3. RULES
──────────────────────────────
• Use unambiguous, deterministic language
• No implementation code or pseudocode
• Names must be consistent across features, API, and DB
• Ensure API fields match database fields
• User can only access their own tasks
• Reference related specs using @specs/…

──────────────────────────────
4. COMPLETION CRITERIA
──────────────────────────────
Mark specification complete only when:

• All Task CRUD features are fully specified
• API endpoints, database models, and feature descriptions are complete
• No ambiguity remains
• Ready for Claude Code implementation in Phase II

## RESPONSE_TEXT

Created comprehensive specifications for the Task CRUD features for Phase II of the Todo Full-Stack Web Application:

1. Feature Specification (specs/task-crud/spec.md):
   - Defined functional requirements for Create, Read, Update, Delete, and Toggle Completion operations
   - Included user scenarios and success criteria
   - Added constraints, assumptions, and validation rules

2. API Specification (specs/api/rest-endpoints.md):
   - Defined REST endpoints for all CRUD operations with proper authentication
   - Specified request/response schemas for each endpoint
   - Included error handling and authorization requirements
   - Ensured user ownership enforcement across all operations

3. Database Specification (specs/database/schema.md):
   - Designed database schema with users and tasks tables
   - Defined columns, types, primary keys, and foreign keys
   - Added indexes for performance optimization
   - Implemented ownership constraints to ensure data isolation

4. Quality Checklist (specs/task-crud/checklists/requirements.md):
   - Created validation checklist to ensure spec completeness
   - Verified all requirements meet quality standards

All specifications are consistent with the constitution and ready for implementation in Phase II.