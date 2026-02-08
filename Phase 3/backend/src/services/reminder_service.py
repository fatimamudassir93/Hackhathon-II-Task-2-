from sqlmodel import select
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.reminder import Reminder
from ..models.task import Task


class ReminderService:

    @staticmethod
    async def schedule_reminder(
        user_id: str, task_id: str, remind_at_str: str, db_session: AsyncSession
    ) -> dict:
        # Verify task exists and belongs to user
        result = await db_session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        task = result.first()
        if not task:
            return {"error": "Task not found"}

        # Parse and validate datetime
        try:
            remind_at = datetime.fromisoformat(remind_at_str.replace("Z", "+00:00"))
        except ValueError:
            return {"error": "Invalid datetime format. Use ISO 8601 format."}

        if remind_at <= datetime.utcnow():
            return {"error": "Reminder time must be in the future"}

        reminder = Reminder(
            user_id=user_id,
            task_id=task_id,
            remind_at=remind_at,
        )
        db_session.add(reminder)
        await db_session.commit()
        await db_session.refresh(reminder)
        return {"reminder_id": reminder.id, "status": "scheduled"}

    @staticmethod
    async def cancel_reminder(
        user_id: str, reminder_id: str, db_session: AsyncSession
    ) -> dict:
        result = await db_session.exec(
            select(Reminder).where(
                Reminder.id == reminder_id, Reminder.user_id == user_id
            )
        )
        reminder = result.first()
        if not reminder:
            return {"error": "Reminder not found"}

        reminder.status = "cancelled"
        await db_session.commit()
        await db_session.refresh(reminder)
        return {"reminder_id": reminder.id, "status": "cancelled"}

    @staticmethod
    async def list_reminders_for_user(
        user_id: str, db_session: AsyncSession
    ) -> dict:
        result = await db_session.exec(
            select(Reminder).where(Reminder.user_id == user_id)
        )
        reminders = result.all()
        return {
            "reminders": [
                {
                    "id": r.id,
                    "task_id": r.task_id,
                    "remind_at": r.remind_at.isoformat(),
                    "status": r.status,
                }
                for r in reminders
            ]
        }
