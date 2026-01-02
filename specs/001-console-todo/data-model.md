# Data Model: In-Memory Python Console Todo App

**Purpose**: Define task entity structure and validation rules for Phase I implementation
**Date**: 2026-01-01
**Spec**: [spec.md](./spec.md)
**Research**: [research.md](./research.md)

## Entity: Task

### Attributes

| Attribute | Type | Description | Validation | Notes |
|-----------|------|-------------|--------|--------|
| `id` | `int` | Must be sequential starting at 1, unique within session | Primary key for all operations (delete, update, complete) |
| `description` | `str` | Non-empty, whitespace-trimmed, max length: none (console handles overflow) | User-visible text, core value of task |
| `status` | `enum` | Must be either `PENDING` or `COMPLETED` | Determines visual marker (`[ ]` vs `[✔]`) |

### Python Implementation (dataclass)

```python
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    """Task completion status following task invariant #2 (single phase-state)."""
    PENDING = "pending"
    COMPLETED = "completed"

@dataclass
class Task:
    """Task entity representing a single to-do item.

    Attributes:
        id: Unique sequential identifier (task invariant #1)
        description: Non-empty text description
        status: Either PENDING or COMPLETED (task invariant #2)

    Note: Task invariant #3 (append-only history) not applicable to Phase I
    due to lack of persistence, but design supports future extension.
    """
    id: int
    description: str
    status: TaskStatus = TaskStatus.PENDING
```

## State Transitions

Task invariant #2: Every task exists in exactly one phase-state at a time.

### Valid Transitions

```
PENDING → COMPLETED (via `complete` command)
PENDING → PENDING (via `update` command - description change only)
COMPLETED → COMPLETED (via `update` command - description change only)

INVALID TRANSITIONS (task invariant #4 violation):
- PENDING → REMOVED (via `delete` - task is deleted, not state changed)
- COMPLETED → PENDING (cannot mark incomplete - violates immutability)
- COMPLETED → REMOVED (via `delete` - task is deleted, not state changed)
```

### Transition Rules

1. **Add Operation**: Creates new task with `PENDING` status, assigns next sequential ID
2. **Complete Operation**: Transitions task from `PENDING` to `COMPLETED` - **MUST validate task is PENDING first**
3. **Update Operation**: Changes `description` field only - **MUST NOT change status** (to enforce invariant #4)
4. **Delete Operation**: Removes task entirely - not a state transition, task ceases to exist
5. **View Operation**: Read-only - no state transition

## Validation Rules

### Task Description Validation (FR-008)

**Rule**: Task descriptions must be non-empty after whitespace trimming

```python
def validate_description(description: str) -> bool:
    """Validate task description is non-empty.

    Raises:
        ValueError: If description is empty or whitespace-only

    Per FR-008: System MUST validate task descriptions are non-empty
    """
    if not description or description.isspace():
        raise ValueError("Task description cannot be empty")
    return True
```

### Task ID Validation (FR-009)

**Rule**: Task ID must exist in current session

```python
def validate_task_id(task_id: int, tasks: dict[int, Task]) -> Task:
    """Validate task ID exists and return corresponding task.

    Raises:
        KeyError: If task_id does not exist

    Per FR-009: System MUST display clear error messages when
    task identifiers don't exist
    """
    if task_id not in tasks:
        raise KeyError(f"Task {task_id} not found")
    return tasks[task_id]
```

### Completed Task Update Validation (task invariant #4)

**Rule**: Cannot update description of completed task (immutable per invariant #4)

```python
def validate_completed_task_update(task: Task) -> None:
    """Validate that task is not completed before update.

    Raises:
        ValueError: If task is COMPLETED

    Per task invariant #4: Completed tasks are immutable.
    """
    if task.status == TaskStatus.COMPLETED:
        raise ValueError("Cannot update completed tasks (immutable per invariant #4)")
```

## In-Memory Storage Schema

### TaskStore (services/store.py)

```python
from typing import Dict, List
from models.task import Task, TaskStatus

class TaskStore:
    """In-memory task repository with CRUD operations.

    Implements FR-012 (in-memory only) and FR-014 (sequential IDs).
    Provides O(1) operations by task ID using dict.
    Maintains insertion order for view operations.

    Per Phase I: FR-013 (clear all data on exit) - store is
    session-scoped and destroyed with application termination.
    """

    def __init__(self) -> None:
        """Initialize empty task store."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, description: str) -> Task:
        """Add new task with next sequential ID and PENDING status."""
        validate_description(description)
        task = Task(
            id=self._next_id,
            description=description.strip(),
            status=TaskStatus.PENDING
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        """Retrieve task by ID."""
        return validate_task_id(task_id, self._tasks)

    def delete(self, task_id: int) -> None:
        """Remove task from store."""
        validate_task_id(task_id, self._tasks)
        del self._tasks[task_id]

    def update_description(self, task_id: int, new_description: str) -> Task:
        """Update task description (validate not completed first)."""
        task = self.get(task_id)
        validate_completed_task_update(task)
        validate_description(new_description)
        task.description = new_description.strip()
        return task

    def complete(self, task_id: int) -> Task:
        """Mark task as COMPLETED (validate it is PENDING first)."""
        task = self.get(task_id)
        if task.status == TaskStatus.COMPLETED:
            raise ValueError(f"Task {task_id} is already completed")
        task.status = TaskStatus.COMPLETED
        return task

    def get_all(self) -> List[Task]:
        """Return all tasks in insertion order (FR-015)."""
        return [self._tasks[task_id] for task_id in sorted(self._tasks.keys())]

    def get_by_status(self, status: TaskStatus) -> List[Task]:
        """Return tasks filtered by status (for US5 - view by status)."""
        return [task for task in self.get_all() if task.status == status]

    def clear(self) -> None:
        """Remove all tasks (FR-013 - clear on exit)."""
        self._tasks.clear()
        self._next_id = 1
```

## Constitution Compliance

| Invariant | Implementation | Status |
|-----------|----------------|--------|
| #1: Unique identity | Sequential IDs (`self._next_id`) in `TaskStore.add()` | ✅ ENFORCED |
| #2: Single phase-state | `TaskStatus` enum prevents invalid states | ✅ ENFORCED |
| #3: Append-only history | Not applicable (no persistence) | ⚠️ DEFERRED TO PHASE II |
| #4: Completed immutability | `validate_completed_task_update()` raises error on update | ✅ ENFORCED |

## Data Model Validation Checklist

- [x] Task entity defined with all attributes from spec
- [x] Status enum enforces single phase-state invariant
- [x] Sequential ID generation (starts at 1, auto-increment)
- [x] Description validation (non-empty, whitespace-trimmed)
- [x] Task ID validation (existence check before operations)
- [x] Completed task immutability enforced (cannot update)
- [x] In-memory store with O(1) lookups by task ID
- [x] Insertion order maintained for view operations
- [x] Status-based filtering support (for US5)
- [x] Clear operation for FR-013 (exit cleanup)
