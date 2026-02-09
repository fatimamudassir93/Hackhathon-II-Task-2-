from sqlmodel import select
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from chatbot.models.conversation import ConversationMessage


class ConversationService:

    @staticmethod
    async def save_message(
        user_id: str,
        role: str,
        content: str,
        tool_calls: Optional[str],
        db_session: AsyncSession,
    ) -> ConversationMessage:
        msg = ConversationMessage(
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
        )
        db_session.add(msg)
        await db_session.commit()
        await db_session.refresh(msg)
        return msg

    @staticmethod
    async def get_history(
        user_id: str,
        db_session: AsyncSession,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[List[ConversationMessage], int]:
        count_result = await db_session.exec(
            select(ConversationMessage).where(
                ConversationMessage.user_id == user_id
            )
        )
        all_messages = count_result.all()
        total = len(all_messages)

        result = await db_session.exec(
            select(ConversationMessage)
            .where(ConversationMessage.user_id == user_id)
            .order_by(ConversationMessage.created_at)
            .offset(offset)
            .limit(limit)
        )
        return result.all(), total

    @staticmethod
    async def get_recent_messages(
        user_id: str,
        db_session: AsyncSession,
        limit: int = 20,
    ) -> List[ConversationMessage]:
        result = await db_session.exec(
            select(ConversationMessage)
            .where(ConversationMessage.user_id == user_id)
            .order_by(ConversationMessage.created_at.desc())
            .limit(limit)
        )
        messages = result.all()
        return list(reversed(messages))
