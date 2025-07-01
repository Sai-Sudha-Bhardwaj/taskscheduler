# taskScheduler/app/schemas.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime # Important for handling date/time fields

# --- Base Schemas ---
# Common fields for Task
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False # Make optional for updates, default to False
    due_date: Optional[datetime] = None # Optional datetime field

# --- Create Schemas ---
# Schema for creating a new Task (client sends this)
class TaskCreate(TaskBase):
    # No additional fields beyond TaskBase for creation,
    # as owner_id is passed via path parameter and timestamps are DB-generated.
    pass

# Schema for creating a new User
class UserCreate(BaseModel):
    username: str

# --- Update Schemas ---
# Schema for updating an existing Task (all fields optional for partial updates)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None

# --- Response Schemas (for data returned by the API) ---
# Full Task schema for responses (includes DB-generated fields)
class Task(TaskBase):
    id: int
    owner_id: int # The ID of the user who owns this task
    created_at: datetime
    updated_at: datetime

    class Config:
        # Pydantic v2: use from_attributes for ORM compatibility
        from_attributes = True

# Full User schema for responses (can include a list of their tasks)
class User(BaseModel):
    id: int
    username: str
    tasks: List[Task] = [] # List of Task schemas for nested representation

    class Config:
        # Pydantic v2: use from_attributes for ORM compatibility
        from_attributes = True