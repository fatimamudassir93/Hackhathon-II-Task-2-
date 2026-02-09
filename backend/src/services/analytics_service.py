"""
Analytics Service

Provides task analytics and metrics for users.
Per Constitution Principle IV: MCP Tool Contract Enforcement
"""
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.models.task import Task


class AnalyticsService:
    """Service for task analytics and metrics"""

    @staticmethod
    async def count_tasks(user_id: str, db_session: AsyncSession) -> int:
        """
        Count total tasks for a user

        Args:
            user_id: User ID
            db_session: Database session

        Returns:
            Total number of tasks
        """
        statement = select(Task).where(Task.user_id == user_id)
        result = await db_session.execute(statement)
        tasks = result.scalars().all()
        return len(tasks)

    @staticmethod
    async def count_completed_tasks(user_id: str, db_session: AsyncSession) -> int:
        """
        Count completed tasks for a user

        Args:
            user_id: User ID
            db_session: Database session

        Returns:
            Number of completed tasks
        """
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.completed == True
        )
        result = await db_session.execute(statement)
        tasks = result.scalars().all()
        return len(tasks)

    @staticmethod
    async def count_pending_tasks(user_id: str, db_session: AsyncSession) -> int:
        """
        Count pending (incomplete) tasks for a user

        Args:
            user_id: User ID
            db_session: Database session

        Returns:
            Number of pending tasks
        """
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.completed == False
        )
        result = await db_session.execute(statement)
        tasks = result.scalars().all()
        return len(tasks)

    @staticmethod
    async def get_task_statistics(user_id: str, db_session: AsyncSession) -> dict:
        """
        Get comprehensive task statistics for a user

        Args:
            user_id: User ID
            db_session: Database session

        Returns:
            Dictionary with total, completed, pending counts and completion rate
        """
        total = await AnalyticsService.count_tasks(user_id, db_session)
        completed = await AnalyticsService.count_completed_tasks(user_id, db_session)
        pending = await AnalyticsService.count_pending_tasks(user_id, db_session)

        completion_rate = (completed / total * 100) if total > 0 else 0.0

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": round(completion_rate, 2)
        }
