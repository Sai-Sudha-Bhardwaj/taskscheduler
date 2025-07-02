# app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None # 'sub' in JWT will be the email/username

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr # Use EmailStr for email validation

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    # Allow partial updates: email and password are optional
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    tasks: List["Task"] = [] # Type hint for relationship

    class Config:
        from_attributes = True # For Pydantic v2+, use from_attributes. For v1, use orm_mode = True

# --- Task Schemas ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    # Allow partial updates for tasks
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None

class Task(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # For Pydantic v2+, use from_attributes. For v1, use orm_mode = True

# Update forward references for Pydantic (needed if classes refer to each other)
# This line is crucial for the `tasks: List["Task"]` in the User schema
User.model_rebuild()