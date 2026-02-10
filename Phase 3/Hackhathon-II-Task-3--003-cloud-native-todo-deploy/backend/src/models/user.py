from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class UserBase(SQLModel):
    email: str
    name: str

class User(UserBase, table=True):
    __tablename__ = "user"

    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(sa_column_kwargs={"unique": True})
    name: str
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None