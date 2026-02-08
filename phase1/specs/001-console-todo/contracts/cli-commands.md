# CLI Contracts: In-Memory Python Console Todo App

**Purpose**: Define command-line interface contracts for user interactions
**Date**: 2026-01-01
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Command Overview

The application supports five core commands following constitution "intent-expressing commands" principle. All commands provide immediate visual feedback (FR-007) and explanatory errors (FR-009, FR-010).

### Command Syntax

```
todo add <description>
todo delete <id>
todo update <id> <description>
todo complete <id>
todo view [--pending | --completed]
```

## Command Contracts

### 1. Add Task

**Command**: `todo add <description>`

**Inputs**:
- `<description>`: Non-empty string (required)

**Success Response**:
```
Task 1 added: "<description>"
```
Followed by updated task list display (per `todo view`)

**Error Responses**:

| Error Condition | Error Message | Resolution |
|-----------------|---------------|------------|
| Empty description | Error: Task description cannot be empty | Provide a non-empty description |
| Whitespace-only description | Error: Task description cannot be empty | Provide a non-empty description |

**Acceptance Scenarios** (from spec US1):
- Given empty list, when add "Buy groceries", then task appears with `[ ]` marker and confirmation displays
- Given 1 pending task, when add "Finish report", then list shows 2 tasks with unique IDs and pending markers
- Given 10 pending tasks, when add "Email client", then task appears as 11th item with proper framing

**Success Criteria Mapping**: SC-001 (add under 1 second)

---

### 2. Delete Task

**Command**: `todo delete <id>`

**Inputs**:
- `<id>`: Task ID (integer, required)

**Success Response**:
```
Task <id> deleted: "<description>"
```
Followed by updated task list display

**Error Responses**:

| Error Condition | Error Message | Resolution |
|-----------------|---------------|------------|
| Task ID not found | Error: Task <id> not found. View available tasks with `todo view` | Provide valid task ID |
| Invalid ID format | Error: Invalid task ID format. Must be an integer | Provide integer ID |

**Acceptance Scenarios** (from spec US3):
- Given 3 tasks [1,2,3], when delete 2, then list shows [1,3] with order maintained
- Given completed task 1 and pending task 2, when delete 1, then only task 2 remains
- Given 1 task, when delete that task, then list shows "No tasks" message

**Success Criteria Mapping**: None (P2 feature)

---

### 3. Update Task Description

**Command**: `todo update <id> <description>`

**Inputs**:
- `<id>`: Task ID (integer, required)
- `<description>`: New description (non-empty string, required)

**Success Response**:
```
Task <id> updated: "<old description>" → "<new description>"
```
Followed by updated task list display

**Error Responses**:

| Error Condition | Error Message | Resolution |
|-----------------|---------------|------------|
| Task ID not found | Error: Task <id> not found. View available tasks with `todo view` | Provide valid task ID |
| Task is completed | Error: Cannot update completed tasks (immutable per invariant #4) | Cannot modify completed task |
| Empty description | Error: Task description cannot be empty | Provide non-empty description |
| Invalid ID format | Error: Invalid task ID format. Must be an integer | Provide integer ID |

**Acceptance Scenarios** (from spec US4):
- Given task 1 "Buy groceri", when update to "Buy groceries", then description updates, status unchanged
- Given completed task 3, when update description, then error displays (immutable)
- Given update with empty description, then error explains cannot be empty, task unchanged

**Success Criteria Mapping**: None (P2 feature)

---

### 4. Complete Task

**Command**: `todo complete <id>`

**Inputs**:
- `<id>`: Task ID (integer, required)

**Success Response**:
```
Task <id> marked as completed: "<description>"
```
Followed by updated task list display

**Error Responses**:

| Error Condition | Error Message | Resolution |
|-----------------|---------------|------------|
| Task ID not found | Error: Task <id> not found. View available tasks with `todo view` | Provide valid task ID |
| Task already completed | Error: Task <id> is already completed | Task is already completed |
| Invalid ID format | Error: Invalid task ID format. Must be an integer | Provide integer ID |

**Acceptance Scenarios** (from spec US2):
- Given 3 pending tasks, when complete 2, then task 2 status changes to `[✔]`, others remain pending
- Given 5 tasks [1-5], when complete 5, then task 5 shows `[✔]`, tasks 1-4 show `[ ]`
- Given mark task complete, when view again, then task still shows `[✔]` (not removed)

**Success Criteria Mapping**: SC-003 (complete under 1 second)

---

### 5. View Tasks

**Command**: `todo view [--pending | --completed]`

**Inputs**:
- `--pending` (optional): Show only pending tasks
- `--completed` (optional): Show only completed tasks
- Default (no flags): Show all tasks

**Success Response**:

**When tasks exist**:
```
┌─────────────────────────────────────────────────────┐
│ TODO LIST                                            │
├─────────────────────────────────────────────────────┤
│ [ ] 1: Buy groceries                                 │
│ [✔] 2: Finish report                                 │
│ [ ] 3: Email client                                  │
└─────────────────────────────────────────────────────┘
3 tasks total (1 pending, 2 completed)
```

**When no tasks exist**:
```
┌─────────────────────────────────────────────────────┐
│ TODO LIST                                            │
├─────────────────────────────────────────────────────┤
│ No tasks                                             │
└─────────────────────────────────────────────────────┘
```

**Error Responses**: None (read-only operation, cannot fail)

**Acceptance Scenarios** (from spec US1, US5):
- Given empty list, when view, then displays "No tasks" message
- Given 3 pending tasks, when view `--pending`, then only those 3 tasks show
- Given 5 tasks (3 pending, 2 completed), when view `--completed`, then only 2 completed show

**Success Criteria Mapping**:
- SC-002 (view under 100ms)
- SC-004 (task state visually distinguishable)

---

## Frame and Formatting Contract

### Console Frame (FR-002)

**Specifications**:
- Width: 80 columns minimum (assumption from spec)
- Style: ASCII box-drawing characters
- Fallback: Simple borders (`|` and `-`) if Unicode unsupported
- Padding: 1 space on each side of content
- Header: "TODO LIST"
- Footer: Task summary count

**Frame Structure**:
```
┌─────────────────────────────────────────────────────┐
│ <header>                                             │
├─────────────────────────────────────────────────────┤
│ <task lines>                                         │
└─────────────────────────────────────────────────────┘
<footer>
```

### Task Line Format

**Format**: `[status] ID: description`

Where:
- `[status]` = `[ ]` for pending, `[✔]` for completed
- `ID` = sequential task identifier (right-aligned in 3 chars: ` 1`, `10`, `100`)
- `description` = task text (word-wrapped if exceeds frame width)

**Example**:
```
[ ]   1: Buy groceries
[✔]   2: Finish report
```

### ANSI Color Contract (FR-011)

**Color Scheme**:

| Element | Color | Purpose |
|---------|-------|---------|
| Frame borders | Dim gray | Subtle structure |
| Header text | Bright white | Section emphasis |
| Pending status `[ ]` | Yellow | Attention needed |
| Completed status `[✔]` | Green | Completion |
| Task ID | Cyan | Identifier |
| Error messages | Red | Error indication |
| Success messages | Green | Confirmation |

**Fallback Behavior**:
- If `sys.stdout.isatty()` returns `False`, disable all ANSI codes
- If terminal capability detection fails, default to no color
- Always display text (color is optional enhancement per FR-011)

---

## Performance Contracts

### Response Time Requirements

| Operation | Target | Success Criteria |
|-----------|--------|------------------|
| Application startup | <1 second | SC-007 |
| View command | <100ms | SC-002 |
| Add task | <1 second | SC-001 |
| Complete task | <1 second | SC-003 |
| Delete task | <1 second | (No SC specified) |
| Update task | <1 second | (No SC specified) |

### Memory Constraints

- **Maximum**: <100MB per technical context (plan.md)
- **Typical**: <10MB for 1000 tasks
- **Per Task**: ~200 bytes (id + description + status + dict overhead)

---

## Constitution Compliance Verification

| Principle | Contract Enforcement | Status |
|-----------|---------------------|--------|
| **Continuity** | Commands designed for future extensibility to Phase II | ✅ |
| **Transparency** | Every command displays confirmation or error message | ✅ |
| **Determinism** | No randomness in outputs, sequential IDs | ✅ |
| **Human-First UX** | Simple verb commands, clear error messages with resolutions | ✅ |
| **Progressive Enhancement** | Optional flags (`--pending`, `--completed`) degrade gracefully | ✅ |

| Command Philosophy | Contract Enforcement | Status |
|-------------------|---------------------|--------|
| Intent-expressing | Verbs express user intent (add, delete, update, complete, view) | ✅ |
| No hidden side effects | All side effects confirmed in output | ✅ |
| Reversible or auditable | Not reversible (no persistence), but auditable via confirmations | ✅ |
| Explanatory errors | All errors include resolution suggestions | ✅ |
