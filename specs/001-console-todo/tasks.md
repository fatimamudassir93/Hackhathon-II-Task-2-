---

description: "Task list template for feature implementation"
---

# Tasks: In-Memory Python Console Todo App

**Input**: Design documents from `/specs/001-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md (required), contracts/cli-commands.md (required)

**Tests**: Tests are OPTIONAL per feature specification. Only include tests if explicitly requested by user.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure per plan.md

<!-- ============================================================================
   IMPORTANT: Tasks are organized by user story with setup and foundational
   phases to support independent implementation and testing.
   Each user story phase is a complete, independently testable increment.
   ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure per implementation plan
- [ ] T002 Initialize Python project with standard library dependencies
- [ ] T003 [P] Create placeholder __init__.py files in all source directories

**Checkpoint**: Project structure ready - foundational components can now be implemented

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create Task entity in src/models/task.py (dataclass with id, description, status)
- [ ] T005 Create TaskStatus enum in src/models/task.py (PENDING, COMPLETED)
- [ ] T006 Create TaskStore class in src/services/store.py (in-memory dict with CRUD operations)
- [ ] T007 Create validation functions in src/services/validator.py (description, task_id, completed task checks)
- [ ] T008 [P] Create ConsoleRenderer class in src/ui/renderer.py (ANSI colors, frame rendering)
- [ ] T009 Create app.py entry point with argparse command routing
- [ ] T010 Create cli.py placeholder for future arg parsing (simple commands: add, delete, update, complete, view)
- [ ] T011 Create placeholder tests directory structure: tests/unit/, tests/integration/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks and view them in a clean, organized list.

**Independent Test**: Can be fully tested by running `python src/app.py add "Buy groceries"` and seeing task appear with `[ ]` marker.

### Implementation for User Story 1

- [ ] T012 Create validate_description function in src/services/validator.py (checks non-empty after whitespace trim)
- [ ] T013 Add add method to TaskStore in src/services/store.py (assigns next sequential ID, PENDING status)
- [ ] T014 Create handle_add function in src/commands/add.py (calls store.add(), validates, returns success/error message)
- [ ] T015 [P] Add _color method to ConsoleRenderer in src/ui/renderer.py (applies ANSI codes if enabled)
- [ ] T016 [P] Add render_frame method to ConsoleRenderer in src/ui/renderer.py (draws ASCII box with header and tasks)
- [ ] T017 [P] Add _format_task_line method to ConsoleRenderer in src/ui/renderer.py (formats: `[status] ID: description`)
- [ ] T018 Integrate add command in app.py routing (maps 'add' subcommand to handle_add)
- [ ] T019 Integrate view command in app.py routing (maps 'view' subcommand to handle_view)

**Checkpoint**: At this point, User Story 1 (Add and View) should be fully functional and testable independently

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P1) 🎯 MVP

**Goal**: Enable users to mark tasks as completed with visible status change from `[ ]` to `[✔]`.

**Independent Test**: Can be fully tested by having multiple tasks, running `python src/app.py complete 2`, and verifying status marker changes.

### Implementation for User Story 2

- [ ] T020 Add validate_completed_task_update function in src/services/validator.py (raises error if task is COMPLETED)
- [ ] T021 Add complete method to TaskStore in src/services/store.py (validates PENDING status, transitions to COMPLETED)
- [ ] T022 Create handle_complete function in src/commands/complete.py (calls store.complete(), validates, returns confirmation)
- [ ] T023 Update _format_task_line in ConsoleRenderer to handle COMPLETED status (`[✔]` marker in green)
- [ ] T024 Integrate complete command in app.py routing (maps 'complete' subcommand to handle_complete)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Delete Tasks (Priority: P2)

**Goal**: Enable users to remove tasks from list with confirmation.

**Independent Test**: Can be fully tested by having multiple tasks, deleting one via `python src/app.py delete 2`, and verifying it no longer appears.

### Implementation for User Story 3

- [ ] T025 Add delete method to TaskStore in src/services/store.py (validates task_id exists, removes from dict)
- [ ] T026 Create handle_delete function in src/commands/delete.py (calls store.delete(), validates, returns confirmation with description)
- [ ] T027 Integrate delete command in app.py routing (maps 'delete' subcommand to handle_delete)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task Description (Priority: P2)

**Goal**: Enable users to correct task descriptions without deleting and recreating.

**Independent Test**: Can be fully tested by having a task, running `python src/app.py update 1 "Buy groceries"`, and verifying description updates while status unchanged.

### Implementation for User Story 4

- [ ] T028 Add update_description method to TaskStore in src/services/store.py (validates not COMPLETED, validates new description, updates)
- [ ] T029 Create handle_update function in src/commands/update.py (calls store.update_description(), validates, returns confirmation with old→new description)
- [ ] T030 Integrate update command in app.py routing (maps 'update' subcommand to handle_update)

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - View Tasks by Status (Priority: P3)

**Goal**: Enable users to filter view by status (pending only or completed only).

**Independent Test**: Can be fully tested by having mixed tasks, running `python src/app.py view --pending` and verifying only pending tasks appear.

### Implementation for User Story 5

- [ ] T031 Add get_by_status method to TaskStore in src/services/store.py (filters tasks by TaskStatus, returns list)
- [ ] T032 [P] Add --pending argument to view subcommand in app.py
- [ ] T033 [P] Add --completed argument to view subcommand in app.py
- [ ] T034 Update handle_view function in src/commands/view.py (accepts optional status_filter, calls appropriate store method)
- [ ] T035 [P] Add render_frame method to ConsoleRenderer to support status filtering (shows filtered tasks or all)
- [ ] T036 Update render_frame in ConsoleRenderer to display task summary footer (e.g., "3 tasks total (1 pending, 2 completed)")

**Checkpoint**: At this point, ALL User Stories (1-5) should be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T037 Add help text to app.py (displays command usage and examples)
- [ ] T038 [P] Add __all__ to src/app.py for module imports
- [ ] T039 [P] Add __all__ to src/models/__init__.py for Task and TaskStatus exports
- [ ] T040 [P] Add __all__ to src/services/__init__.py for TaskStore and validator exports
- [ ] T041 [P] Add __all__ to src/commands/__init__.py for command handler exports
- [ ] T042 [P] Add __all__ to src/ui/__init__.py for ConsoleRenderer exports
- [ ] T043 Add README.md with usage examples
- [ ] T044 Verify all functional requirements met (FR-001 through FR-017)
- [ ] T045 Verify all success criteria achievable (SC-001 through SC-009)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational (Phase 2) - No dependencies on other stories
  - User Story 2 (P1): Can start after Foundational (Phase 2) - Depends on US1 for Task entity, but can proceed in parallel for command handlers
  - User Story 3 (P2): Can start after Foundational (Phase 2) - Depends on US1 for Task entity, but can proceed in parallel for command handlers
  - User Story 4 (P2): Can start after Foundational (Phase 2) - Depends on US1 for Task entity, but can proceed in parallel for command handlers
  - User Story 5 (P3): Can start after Foundational (Phase 2) - Depends on US1 for Task entity and store methods
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) completion only
- **User Story 2 (P1)**: Depends on Foundational (Phase 2) + US1 completion for Task entity and status markers
- **User Story 3 (P2)**: Depends on Foundational (Phase 2) + US1 for Task entity and store
- **User Story 4 (P2)**: Depends on Foundational (Phase 2) + US1 for Task entity and store
- **User Story 5 (P3)**: Depends on Foundational (Phase 2) + US1 for Task entity and store

### Within Each User Story

- Foundation tasks must be complete before any user story work begins
- Model (Task) created in US1 reused by all subsequent stories
- Store (TaskStore) created in US1 reused by all subsequent stories
- Tests (if included) MUST be written and FAIL before implementation
- Entity classes before service methods before command handlers
- Command handlers before app.py integration

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T001, T002, T003)
- All Foundational tasks marked [P] can run in parallel (T004, T005, T006, T007, T008, T009, T010, T011)
- Within US1: T015 and T016 can run in parallel
- Within US2: T023 can run in parallel to US1
- Within US3: T027 can run in parallel to US1
- Within US4: T030 can run in parallel to US1
- Within US5: T032 and T033 can run in parallel to US1
- Polish tasks (T039, T040, T041, T042, T043) can all run in parallel

---

## Implementation Strategy

### MVP First (User Stories 1-2 only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T011)
3. Complete Phase 3: User Story 1 - Add and View (T012-T019)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Complete Phase 4: User Story 2 - Mark Complete (T020-T024)
6. **STOP and VALIDATE**: Test User Stories 1 AND 2 together
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Add/View) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Mark Complete) → Test independently → Deploy/Demo
4. Add User Stories 3-5 (Delete, Update, View Filter) → Each adds value without breaking previous stories
5. Each story adds value without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (if tests requested)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
