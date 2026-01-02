def validate_description(description: str) -> bool:
    """Validate task description is non-empty.

    Raises:
        ValueError: If description is empty or whitespace-only

    Per FR-008: System MUST validate task descriptions are non-empty
    """
    if not description or description.isspace():
        raise ValueError("Task description cannot be empty")
    return True


def validate_task_id(task_id: int, tasks: dict) -> None:
    """Validate task ID exists and return corresponding task.

    Raises:
        KeyError: If task_id does not exist

    Per FR-009: System MUST display clear error messages when
    task identifiers don't exist
    """
    if task_id not in tasks:
        raise KeyError(f"Task {task_id} not found")
    return tasks[task_id]


def validate_completed_task_update(task) -> None:
    """Validate that task is not completed before update.

    Raises:
        ValueError: If task is COMPLETED

    Per task invariant #4: Completed tasks are immutable.
    """
    if task.status == TaskStatus.COMPLETED:
        raise ValueError("Cannot update completed tasks (immutable per invariant #4)")
