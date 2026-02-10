---
id: 2
title: Phase 3 AI Chatbot Constitution
stage: constitution
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: none
branch: 001-console-todo
user: shoai
command: /sp.constitution
labels: ["constitution", "phase3", "ai-chatbot", "agents", "mcp"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

# Phase 3: Todo AI Chatbot Constitution

## Overview
- AI chatbot to manage todos via natural language.
- Frontend: ChatKit UI | Backend: FastAPI + OpenAI Agents SDK | DB: Neon PostgreSQL
- Stateless server; conversation persisted in DB.
- Authentication: Better Auth.

## Agents
| Agent | Purpose | Key Skills |
|-------|--------|------------|
| Task Agent | Task CRUD | add_task, list_tasks, update_task, complete_task, delete_task |
| Reminder Agent | Manage reminders | schedule_reminder, cancel_reminder, list_reminders |
| User/Auth Agent | Authentication | signup, login, logout, password_reset |
| Tag/Category Agent | Organize tasks | add_tag, remove_tag, list_tags, filter_tasks_by_tag |
| Analytics Agent | Insights | count_tasks, tasks_done, tasks_pending |
| Integration Agent | Optional external | Calendar/Slack/Email sync |

## MCP Tools
- `add_task(user_id, title, description)` → task_id, status
- `list_tasks(user_id, status)` → array of tasks
- `update_task(user_id, task_id, title, description)` → task_id, status
- `complete_task(user_id, task_id)` → task_id, status
- `delete_task(user_id, task_id)` → task_id, status
- `schedule_reminder`, `cancel_reminder`, `list_reminders`
- `add_tag`, `remove_tag`, `list_tags`, `filter_tasks_by_tag`

## Conversation Rules
- Map natural language to MCP tools (e.g., "Add task" → add_task).
- Confirm actions, handle errors, maintain conversation context.
- Stateless server; all state in DB.

## Deliverables
- `/frontend` → ChatKit UI
- `/backend` → FastAPI + Agents SDK + MCP
- `/specs` → Agents & MCP tools Markdown files
- Database migration scripts
- Fully functional AI chatbot

## Claude Execution
- Generate agents and MCP tools as Markdown in `/specs`.
- Break project into tasks for Agentic Dev Stack workflow.
- No manual coding; output ready-to-run files.

## Response snapshot

Amended constitution from v2.0.0 to v3.0.0 (MAJOR bump). Complete project scope change from Phase II full-stack web app to Phase III AI chatbot with multi-agent architecture. Eight principles defined: Technology Binding, Agent Architecture, Authentication (Better Auth), MCP Tool Contract, Test-First, Conversation Statelessness, Feature Scope Lock, and Spec-Driven Execution. All MCP tool signatures documented. Agent table with 6 agents codified. Frontend/Backend rules updated for ChatKit UI and OpenAI Agents SDK. Quality gates updated for agent routing, conversation persistence, and stateless server verification.

## Outcome

- ✅ Impact: Constitution fully rewritten for Phase III AI chatbot scope
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md (overwritten)
- 🔁 Next prompts: /sp.specify to create feature spec for first chatbot feature
- 🧠 Reflection: Major version bump justified by complete scope change; all 8 principles are declarative and testable

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate template sync after first /sp.plan run
