from sqlmodel import select, Session
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound

class TaskService:
    """Service class for task-related operations with user authorization"""

    @staticmethod
    async def get_tasks_by_user_id(user_id: str, db_session: AsyncSession) -> List[Task]:
        """
        Get all tasks for a specific user
        Args:
            user_id: User ID to get tasks for
            db_session: Database session
        Returns:
            List of tasks for the user
        """
        result = await db_session.exec(
            select(Task).where(Task.user_id == user_id)
        )
        return result.all()

    @staticmethod
    async def get_task_by_id_and_user_id(task_id: str, user_id: str, db_session: AsyncSession) -> Optional[Task]:
        """
        Get a specific task by ID and user ID
        Args:
            task_id: Task ID to get
            user_id: User ID that should own the task
            db_session: Database session
        Returns:
            Task if found and user owns it, None otherwise
        """
        result = await db_session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.first()

    @staticmethod
    async def create_task_for_user(task_data: TaskCreate, user_id: str, db_session: AsyncSession) -> Task:
        """
        Create a task for a specific user
        Args:
            task_data: Task creation data
            user_id: User ID that will own the task
            db_session: Database session
        Returns:
            Created task
        """
        db_task = Task(
            **task_data.dict(),
            user_id=user_id
        )

        db_session.add(db_task)
        await db_session.commit()
        await db_session.refresh(db_task)

        return db_task

    @staticmethod
    async def update_task_for_user(task_id: str, task_update: TaskUpdate, user_id: str, db_session: AsyncSession) -> Optional[Task]:
        """
        Update a task for a specific user
        Args:
            task_id: Task ID to update
            task_update: Task update data
            user_id: User ID that owns the task
            db_session: Database session
        Returns:
            Updated task if user owns it, None otherwise
        """
        # Get the existing task to update
        db_task = await TaskService.get_task_by_id_and_user_id(task_id, user_id, db_session)
        if not db_task:
            return None

        # Update the task with new values
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        await db_session.commit()
        await db_session.refresh(db_task)

        return db_task

    @staticmethod
    async def delete_task_for_user(task_id: str, user_id: str, db_session: AsyncSession) -> bool:
        """
        Delete a task for a specific user
        Args:
            task_id: Task ID to delete
            user_id: User ID that owns the task
            db_session: Database session
        Returns:
            True if task was deleted, False if user doesn't own the task
        """
        # Get the existing task to delete
        db_task = await TaskService.get_task_by_id_and_user_id(task_id, user_id, db_session)
        if not db_task:
            return False

        await db_session.delete(db_task)
        await db_session.commit()

        return True

    @staticmethod
    async def update_task_completion_for_user(task_id: str, completed: bool, user_id: str, db_session: AsyncSession) -> Optional[Task]:
        """
        Update the completion status of a task for a specific user
        Args:
            task_id: Task ID to update
            completed: New completion status
            user_id: User ID that owns the task
            db_session: Database session
        Returns:
            Updated task if user owns it, None otherwise
        """
        # Get the existing task to update
        db_task = await TaskService.get_task_by_id_and_user_id(task_id, user_id, db_session)
        if not db_task:
            return None

        # Update the completion status
        db_task.completed = completed

        await db_session.commit()
        await db_session.refresh(db_task)

        return db_task