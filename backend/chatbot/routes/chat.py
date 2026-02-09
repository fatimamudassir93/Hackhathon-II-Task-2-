from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Path
from src.database.session import get_db_session
from src.dependencies.auth import get_current_user_id, verify_user_id_match_path
from chatbot.schemas.chat import ChatRequest, ChatResponse, ChatHistoryResponse, ChatMessageOut
from chatbot.services.chat_service import ChatService
from chatbot.services.conversation_service import ConversationService
import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def send_chat_message(
    chat_request: ChatRequest,
    user_id: str = Path(..., description="User ID"),
    current_user_id: str = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session),
):
    verify_user_id_match_path(user_id, current_user_id)

    try:
        result = await ChatService.process_message(
            user_id=user_id,
            message=chat_request.message,
            db_session=db_session,
        )
        return ChatResponse(
            reply=result["reply"],
            tool_calls=result.get("tool_calls", []),
        )
    except Exception as e:
        logger.error(f"Chat processing failed: {e}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}",
        )


@router.get("/{user_id}/chat/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    user_id: str = Path(..., description="User ID"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    current_user_id: str = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session),
):
    verify_user_id_match_path(user_id, current_user_id)

    messages, total = await ConversationService.get_history(
        user_id=user_id,
        db_session=db_session,
        limit=limit,
        offset=offset,
    )

    return ChatHistoryResponse(
        messages=[
            ChatMessageOut(
                id=m.id,
                role=m.role,
                content=m.content,
                tool_calls=m.tool_calls,
                created_at=m.created_at,
            )
            for m in messages
        ],
        total=total,
    )
