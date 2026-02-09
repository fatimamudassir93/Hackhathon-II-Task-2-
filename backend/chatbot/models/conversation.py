from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class ConversationMessage(SQLModel, table=True):
    __tablename__ = "conversation_messages"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    user_id: str = Field(index=True)
    role: str  # "user" or "assistant"
    content: str
    tool_calls: Optional[str] = None  # JSON-serialized array
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class ConversationMessageRead(SQLModel):
    id: str
    user_id: str
    role: str
    content: str
    tool_calls: Optional[str] = None
    created_at: datetime
