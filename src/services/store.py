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

    def add(self, title: str, description: str) -> Task:
        """Add new task with next sequential ID and PENDING status."""
        if not title or title.isspace():
            raise ValueError("Task title cannot be empty")
        if not description or description.isspace():
            raise ValueError("Task description cannot be empty")
        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description.strip(),
            status=TaskStatus.PENDING
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        """Retrieve task by ID."""
        if task_id not in self._tasks:
            raise KeyError(f"Task {task_id} not found")
        return self._tasks[task_id]

    def delete(self, task_id: int) -> None:
        """Remove task from store."""
        if task_id not in self._tasks:
            raise KeyError(f"Task {task_id} not found")
        del self._tasks[task_id]

    def update(self, task_id: int, title: str = None, description: str = None) -> Task:
        """Update task title and/or description (invariant #4: completed tasks immutable)."""
        task = self.get(task_id)
        if task.status == TaskStatus.COMPLETED:
            raise ValueError("Cannot update completed tasks (immutable per invariant #4)")

        if title is not None:
            if not title or title.isspace():
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()

        if description is not None:
            if not description or description.isspace():
                raise ValueError("Task description cannot be empty")
            task.description = description.strip()

        if title is None and description is None:
            raise ValueError("Must provide at least one field to update")

        return task

    def toggle_status(self, task_id: int) -> Task:
        """Toggle task status between PENDING and COMPLETED."""
        task = self.get(task_id)
        if task.status == TaskStatus.COMPLETED:
            task.status = TaskStatus.PENDING
        else:
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
