from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = "medium"  # low, medium, high
    due_date: Optional[datetime] = None

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")  # Foreign key to users table
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = "medium"  # low, medium, high
    due_date: Optional[datetime] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class TaskRead(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class TaskCreate(TaskBase):
    title: str

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None  # low, medium, high
    due_date: Optional[datetime] = None