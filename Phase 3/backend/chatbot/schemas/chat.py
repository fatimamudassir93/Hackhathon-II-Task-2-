from pydantic import BaseModel, field_validator
from typing import List, Optional, Any
from datetime import datetime


class ChatRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()


class ToolCallInfo(BaseModel):
    tool: str
    args: Optional[dict[str, Any]] = {}
    result: Optional[dict[str, Any]] = {}


class ChatResponse(BaseModel):
    reply: str
    tool_calls: List[ToolCallInfo] = []


class ChatMessageOut(BaseModel):
    id: str
    role: str
    content: str
    tool_calls: Optional[str] = None
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessageOut]
    total: int
