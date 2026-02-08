from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class Reminder(SQLModel, table=True):
    __tablename__ = "reminders"

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    user_id: str = Field(foreign_key="user.id")
    task_id: str = Field(foreign_key="task.id")
    remind_at: datetime
    status: str = Field(default="active")  # active, cancelled, sent
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class ReminderRead(SQLModel):
    id: str
    user_id: str
    task_id: str
    remind_at: datetime
    status: str
    created_at: datetime
