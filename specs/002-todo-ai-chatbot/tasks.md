# Tasks: Todo AI Chatbot

**Input**: Design documents from `/specs/002-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included per Constitution Principle V (Test-First NON-NEGOTIABLE).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/` at repository root

---

## Phase 1: Setup

**Purpose**: Install new dependencies and create project scaffolding

- [x] T001 Add `openai-agents` to backend/requirements.txt
- [x] T002 [P] Add OPENAI_API_KEY to backend/src/config.py Settings class
- [x] T003 [P] Install `@chatscope/chat-ui-kit-react` in frontend/package.json via npm
- [x] T004 [P] Create backend/src/agents/__init__.py (empty init)
- [x] T005 [P] Create backend/src/tools/__init__.py (empty init)
- [x] T006 [P] Create backend/tests/test_tools/__init__.py (empty init)
- [x] T007 [P] Create backend/tests/test_agents/__init__.py (empty init)
- [x] T008 [P] Create backend/tests/test_services/__init__.py (empty init)
- [x] T009 [P] Create backend/tests/test_routes/__init__.py (empty init)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: New database models and services that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T010 Create ConversationMessage SQLModel in backend/src/models/conversation.py per data-model.md (id, user_id, role, content, tool_calls, created_at)
- [x] T011 [P] Create Tag SQLModel in backend/src/models/tag.py per data-model.md (id, user_id, name, created_at with unique constraint on user_id+name)
- [x] T012 [P] Create TaskTag SQLModel join table in backend/src/models/tag.py (task_id, tag_id composite PK)
- [x] T013 [P] Create Reminder SQLModel in backend/src/models/reminder.py per data-model.md (id, user_id, task_id, remind_at, status, created_at)
- [x] T014 Register new models (ConversationMessage, Tag, TaskTag, Reminder) in backend/src/main.py on_startup for table creation
- [x] T015 [P] Extend frontend/lib/schema.ts with conversation_message, tag, task_tag, and reminder Drizzle table definitions
- [x] T016 Implement ConversationService in backend/src/services/conversation_service.py (save_message, get_history with pagination, get_recent_messages for agent context)
- [x] T017 Implement ChatService in backend/src/services/chat_service.py (process_message: save user msg, load context, run agent, save response, return reply+tool_calls)
- [x] T018 Create chat request/response schemas in backend/src/schemas/chat.py (ChatRequest with message field, ChatResponse with reply+tool_calls, ChatHistoryResponse with messages+total)

**Checkpoint**: Foundation ready — all models, core services, and schemas in place

---

## Phase 3: User Story 1 — Manage Tasks via Chat (Priority: P1) MVP

**Goal**: Users can add, list, update, complete, and delete tasks through natural language chat messages

**Independent Test**: Send chat messages for each CRUD operation; verify task creation, listing, updating, completing, and deletion with confirmation messages

### Tests for User Story 1

> **Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T019 [P] [US1] Write unit tests for task MCP tools (add_task, list_tasks, update_task, complete_task, delete_task) in backend/tests/test_tools/test_task_tools.py — test success paths, not-found errors, empty title validation
- [ ] T020 [P] [US1] Write integration test for POST /api/{user_id}/chat with task commands in backend/tests/test_routes/test_chat.py — test "Add a task", "Show tasks", "Complete task", "Delete task" flows
- [ ] T021 [P] [US1] Write unit test for triage agent routing task intents to Task Agent in backend/tests/test_agents/test_triage.py

### Implementation for User Story 1

- [x] T022 [P] [US1] Implement task MCP tools (add_task, list_tasks, update_task, complete_task, delete_task) as @function_tool functions in backend/src/tools/task_tools.py — each tool wraps existing TaskService methods per contracts/mcp-tools.md
- [x] T023 [US1] Implement Task Agent with instructions and task tools in backend/src/agents/task_agent.py — agent receives user intent about tasks, calls appropriate tool, returns confirmation
- [x] T024 [US1] Implement Triage Agent in backend/src/agents/triage.py — routes user messages to Task Agent (and later to other specialist agents via handoffs)
- [x] T025 [US1] Implement chat route POST /api/{user_id}/chat in backend/src/routes/chat.py — JWT auth, validate message, call ChatService.process_message, return ChatResponse per contracts/chat-api.md
- [x] T026 [US1] Implement chat history route GET /api/{user_id}/chat/history in backend/src/routes/chat.py — JWT auth, pagination with limit/offset, return ChatHistoryResponse
- [x] T027 [US1] Register chat router in backend/src/main.py (app.include_router)
- [x] T028 [US1] Create chat API client in frontend/lib/chat-api.ts — sendMessage(userId, message, token) and getHistory(userId, token, limit, offset) functions
- [x] T029 [US1] Create ChatMessage component in frontend/components/ChatMessage.tsx — render user and assistant messages with proper styling, timestamps, glassmorphism theme
- [x] T030 [US1] Create ToolCallDisplay component in frontend/components/ToolCallDisplay.tsx — render MCP tool calls inline with message (tool name, result summary)
- [x] T031 [US1] Create ChatInterface component in frontend/components/ChatInterface.tsx — ChatKit MainContainer with MessageList, MessageInput, TypingIndicator, user/bot avatars
- [x] T032 [US1] Create chat page in frontend/app/chat/page.tsx — authenticated page, loads ChatInterface, fetches history on mount, handles send/receive flow
- [x] T033 [US1] Add chat animations to frontend/app/globals.css — message slide-in, typing indicator pulse, tool-call expand animation
- [x] T034 [US1] Add chat navigation link to frontend/components/Navbar.tsx — link to /chat route

**Checkpoint**: User Story 1 fully functional — users can manage tasks via chat. This is the MVP.

---

## Phase 4: User Story 2 — User Authentication (Priority: P2)

**Goal**: Users can sign up, sign in, log out, and reset password; sessions persist across refreshes

**Independent Test**: Sign up a new user, sign in, verify session persistence, log out, test password reset

### Tests for User Story 2

- [ ] T035 [P] [US2] Write integration test for chat endpoint authentication in backend/tests/test_routes/test_chat.py — test 401 without JWT, 403 with wrong user_id, success with valid JWT

### Implementation for User Story 2

- [ ] T036 [US2] Add authentication guards to chat routes in backend/src/routes/chat.py — verify get_current_user_id and verify_user_id_match_path dependencies are applied (reuse existing auth.py dependencies)
- [ ] T037 [US2] Add session-aware redirect in frontend/app/chat/page.tsx — redirect unauthenticated users to sign-in, redirect authenticated users from home to chat
- [ ] T038 [US2] Verify Better Auth session persistence in frontend/app/chat/page.tsx — useSession hook check, show loading state while verifying

**Checkpoint**: Authentication integrated with chat flow — existing Better Auth setup reused

---

## Phase 5: User Story 3 — Organize Tasks with Tags (Priority: P3)

**Goal**: Users can add/remove tags on tasks, list their tags, and filter tasks by tag through chat

**Independent Test**: Add tags to tasks, list tags, filter tasks by tag, remove tags — all through chat

### Tests for User Story 3

- [ ] T039 [P] [US3] Write unit tests for tag MCP tools (add_tag, remove_tag, list_tags, filter_tasks_by_tag) in backend/tests/test_tools/test_tag_tools.py — success paths, task-not-found, tag-not-found, empty tag validation
- [ ] T040 [P] [US3] Write unit tests for TagService in backend/tests/test_services/test_tag_service.py — CRUD operations, unique constraint, cascade delete

### Implementation for User Story 3

- [ ] T041 [US3] Implement TagService in backend/src/services/tag_service.py — add_tag_to_task, remove_tag_from_task, get_tags_for_user, get_tasks_by_tag (all user-scoped, per data-model.md)
- [ ] T042 [US3] Implement tag MCP tools (add_tag, remove_tag, list_tags, filter_tasks_by_tag) as @function_tool functions in backend/src/tools/tag_tools.py — each tool wraps TagService per contracts/mcp-tools.md
- [ ] T043 [US3] Implement Tag Agent with instructions and tag tools in backend/src/agents/tag_agent.py
- [ ] T044 [US3] Register Tag Agent as handoff target in backend/src/agents/triage.py — triage routes tag-related intents to Tag Agent

**Checkpoint**: Tags work through chat — users can organize tasks with labels

---

## Phase 6: User Story 4 — Task Reminders (Priority: P4)

**Goal**: Users can schedule, list, and cancel reminders for tasks through chat

**Independent Test**: Schedule a reminder, list reminders, cancel a reminder — all through chat

### Tests for User Story 4

- [ ] T045 [P] [US4] Write unit tests for reminder MCP tools (schedule_reminder, cancel_reminder, list_reminders) in backend/tests/test_tools/test_reminder_tools.py — success paths, task-not-found, past-datetime rejection, reminder-not-found
- [ ] T046 [P] [US4] Write unit tests for ReminderService in backend/tests/test_services/test_reminder_service.py — CRUD operations, status transitions, future-date validation

### Implementation for User Story 4

- [ ] T047 [US4] Implement ReminderService in backend/src/services/reminder_service.py — schedule_reminder, cancel_reminder, list_reminders_for_user (all user-scoped, validate remind_at is future, per data-model.md)
- [ ] T048 [US4] Implement reminder MCP tools (schedule_reminder, cancel_reminder, list_reminders) as @function_tool functions in backend/src/tools/reminder_tools.py — each tool wraps ReminderService per contracts/mcp-tools.md
- [ ] T049 [US4] Implement Reminder Agent with instructions and reminder tools in backend/src/agents/reminder_agent.py
- [ ] T050 [US4] Register Reminder Agent as handoff target in backend/src/agents/triage.py — triage routes reminder-related intents to Reminder Agent

**Checkpoint**: Reminders work through chat — users can schedule and manage reminders

---

## Phase 7: User Story 5 — Task Analytics (Priority: P5)

**Goal**: Users can ask for task counts (total, done, pending) through chat

**Independent Test**: Create tasks with mixed statuses, query counts through chat

### Tests for User Story 5

- [ ] T051 [P] [US5] Write unit tests for analytics MCP tools (count_tasks, tasks_done, tasks_pending) in backend/tests/test_tools/test_analytics_tools.py — verify correct counts with mixed task statuses

### Implementation for User Story 5

- [ ] T052 [US5] Implement analytics MCP tools (count_tasks, tasks_done, tasks_pending) as @function_tool functions in backend/src/tools/analytics_tools.py — query TaskService for counts, per contracts/mcp-tools.md
- [ ] T053 [US5] Implement Analytics Agent with instructions and analytics tools in backend/src/agents/analytics_agent.py
- [ ] T054 [US5] Register Analytics Agent as handoff target in backend/src/agents/triage.py — triage routes analytics intents to Analytics Agent

**Checkpoint**: Analytics work through chat — users get task insights

---

## Phase 8: User Story 6 — External Integrations (Priority: P6, Optional)

**Goal**: Optional integration with external services (calendar, Slack, email)

**Independent Test**: Connect mock external service, verify sync operations

> **NOTE**: This phase is optional per constitution Feature Scope Lock. Requires explicit user approval before implementation.

- [ ] T055 [US6] Design Integration Agent interface and tool contracts in specs/002-todo-ai-chatbot/contracts/integration-tools.md
- [ ] T056 [US6] Implement Integration Agent stub in backend/src/agents/integration_agent.py — respond with "Integration feature coming soon" until contracts are approved

**Checkpoint**: Integration Agent stubbed — ready for future implementation when approved

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, edge cases, and quality improvements across all stories

- [ ] T057 Add error handling for ambiguous user input in backend/src/agents/triage.py — if no agent matches intent, ask for clarification instead of guessing
- [ ] T058 [P] Add empty message validation in backend/src/routes/chat.py — return 400 for empty or whitespace-only messages
- [ ] T059 [P] Add error handling for database unavailability in backend/src/services/chat_service.py — catch connection errors, return user-friendly message
- [ ] T060 [P] Add loading/typing indicator state management in frontend/components/ChatInterface.tsx — show TypingIndicator while POST is in flight
- [ ] T061 [P] Add inline error display in frontend/components/ChatInterface.tsx — render error messages in chat when backend returns errors
- [ ] T062 Verify conversation history persistence across page refresh in frontend/app/chat/page.tsx — ensure getHistory loads on mount and displays correctly
- [ ] T063 Verify stateless server — restart backend, confirm all tasks/reminders/tags/conversations are intact from DB
- [ ] T064 Run quickstart.md validation checklist — follow setup guide end-to-end and verify all items pass

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 Task Chat (Phase 3)**: Depends on Foundational — core MVP
- **US2 Auth (Phase 4)**: Depends on Foundational — can run in parallel with US1 (auth infrastructure already exists)
- **US3 Tags (Phase 5)**: Depends on Foundational — can run in parallel with US1
- **US4 Reminders (Phase 6)**: Depends on Foundational — can run in parallel with US1
- **US5 Analytics (Phase 7)**: Depends on Foundational — can run in parallel with US1
- **US6 Integrations (Phase 8)**: Depends on all prior stories — optional
- **Polish (Phase 9)**: Depends on US1-US5 being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational — No dependencies on other stories
- **US2 (P2)**: Can start after Foundational — Auth already exists, only need chat guards
- **US3 (P3)**: Can start after Foundational — Independent (Tag models in Foundational)
- **US4 (P4)**: Can start after Foundational — Independent (Reminder model in Foundational)
- **US5 (P5)**: Can start after Foundational — Independent (uses existing TaskService)
- **US6 (P6)**: Optional — defer until all core stories are stable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before tools
- Tools before agents
- Agents before routes/UI
- Backend before frontend for each story

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002-T009)
- All Foundational model tasks marked [P] can run in parallel (T011-T013)
- Once Foundational is complete, US1-US5 backend work can proceed in parallel
- Within each story, test tasks marked [P] can run in parallel
- Frontend chat components (T029, T030) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests in parallel:
Task: "Unit tests for task tools in backend/tests/test_tools/test_task_tools.py"
Task: "Integration test for chat endpoint in backend/tests/test_routes/test_chat.py"
Task: "Triage agent routing test in backend/tests/test_agents/test_triage.py"

# Then launch implementation — tools can parallelize:
Task: "Task MCP tools in backend/src/tools/task_tools.py"

# Then sequential: agent → route → frontend
Task: "Task Agent in backend/src/agents/task_agent.py"
Task: "Triage Agent in backend/src/agents/triage.py"
Task: "Chat route in backend/src/routes/chat.py"

# Then frontend components in parallel:
Task: "ChatMessage in frontend/components/ChatMessage.tsx"
Task: "ToolCallDisplay in frontend/components/ToolCallDisplay.tsx"
Task: "ChatInterface in frontend/components/ChatInterface.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 — Task Chat
4. **STOP and VALIDATE**: Test task CRUD via chat independently
5. Deploy/demo if ready — this is the MVP

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Task Chat) → Test → Deploy/Demo (MVP!)
3. Add US2 (Auth Guards) → Test → Deploy/Demo
4. Add US3 (Tags) → Test → Deploy/Demo
5. Add US4 (Reminders) → Test → Deploy/Demo
6. Add US5 (Analytics) → Test → Deploy/Demo
7. Polish → Final validation → Deploy/Demo
8. (Optional) Add US6 (Integrations) if approved

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US1 (Task Chat) — critical path
   - Developer B: US3 (Tags) + US4 (Reminders) — backend tools
   - Developer C: US5 (Analytics) + US2 (Auth Guards)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US6 (Integrations) is optional per constitution — requires approval
- Existing backend services (TaskService, UserService) are reused by MCP tools
