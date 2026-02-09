from sqlmodel import select
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.tag import Tag, TaskTag
from ..models.task import Task


class TagService:

    @staticmethod
    async def add_tag_to_task(
        user_id: str, task_id: str, tag_name: str, db_session: AsyncSession
    ) -> dict:
        # Verify task exists and belongs to user
        result = await db_session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        task = result.first()
        if not task:
            return {"error": "Task not found"}

        # Find or create the tag
        result = await db_session.exec(
            select(Tag).where(Tag.user_id == user_id, Tag.name == tag_name)
        )
        tag = result.first()
        if not tag:
            tag = Tag(user_id=user_id, name=tag_name)
            db_session.add(tag)
            await db_session.commit()
            await db_session.refresh(tag)

        # Check if already linked
        result = await db_session.exec(
            select(TaskTag).where(
                TaskTag.task_id == task_id, TaskTag.tag_id == tag.id
            )
        )
        if not result.first():
            task_tag = TaskTag(task_id=task_id, tag_id=tag.id)
            db_session.add(task_tag)
            await db_session.commit()

        # Return current tags for the task
        tags = await TagService._get_tags_for_task(task_id, db_session)
        return {"task_id": task_id, "tags": tags}

    @staticmethod
    async def remove_tag_from_task(
        user_id: str, task_id: str, tag_name: str, db_session: AsyncSession
    ) -> dict:
        # Find the tag
        result = await db_session.exec(
            select(Tag).where(Tag.user_id == user_id, Tag.name == tag_name)
        )
        tag = result.first()
        if not tag:
            return {"error": "Tag not found on task"}

        # Find the link
        result = await db_session.exec(
            select(TaskTag).where(
                TaskTag.task_id == task_id, TaskTag.tag_id == tag.id
            )
        )
        task_tag = result.first()
        if not task_tag:
            return {"error": "Tag not found on task"}

        await db_session.delete(task_tag)
        await db_session.commit()

        tags = await TagService._get_tags_for_task(task_id, db_session)
        return {"task_id": task_id, "tags": tags}

    @staticmethod
    async def get_tags_for_user(
        user_id: str, db_session: AsyncSession
    ) -> List[str]:
        result = await db_session.exec(
            select(Tag).where(Tag.user_id == user_id)
        )
        return [t.name for t in result.all()]

    @staticmethod
    async def get_tasks_by_tag(
        user_id: str, tag_name: str, db_session: AsyncSession
    ) -> dict:
        result = await db_session.exec(
            select(Tag).where(Tag.user_id == user_id, Tag.name == tag_name)
        )
        tag = result.first()
        if not tag:
            return {"tasks": [], "tag": tag_name}

        result = await db_session.exec(
            select(Task)
            .join(TaskTag, TaskTag.task_id == Task.id)
            .where(TaskTag.tag_id == tag.id, Task.user_id == user_id)
        )
        tasks = result.all()
        return {
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "completed": t.completed,
                    "priority": t.priority,
                }
                for t in tasks
            ],
            "tag": tag_name,
        }

    @staticmethod
    async def _get_tags_for_task(
        task_id: str, db_session: AsyncSession
    ) -> List[str]:
        result = await db_session.exec(
            select(Tag)
            .join(TaskTag, TaskTag.tag_id == Tag.id)
            .where(TaskTag.task_id == task_id)
        )
        return [t.name for t in result.all()]
