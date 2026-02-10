from sqlmodel import SQLModel, Field, UniqueConstraint
from datetime import datetime
from typing import Optional
import uuid


class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_tag_user_name"),
    )

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True
    )
    user_id: str = Field(index=True)
    name: str = Field(max_length=50)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"

    task_id: str = Field(foreign_key="task.id", primary_key=True)
    tag_id: str = Field(foreign_key="tags.id", primary_key=True)


class TagRead(SQLModel):
    id: str
    user_id: str
    name: str
    created_at: datetime
