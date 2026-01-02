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
        title: Non-empty text title
        description: Non-empty text description
        status: Either PENDING or COMPLETED (task invariant #2)

    Note: Task invariant #3 (append-only history) not applicable to Phase I
    due to lack of persistence, but design supports future extension.
    Invariant #4 (completed immutability) enforced in store layer.
    """
    id: int
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
