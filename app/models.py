# taskScheduler/app/models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # Important for server_default and onupdate timestamps

from .database import Base # Import Base from your database.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

    # Relationship to tasks: one user can have many tasks
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime(timezone=True), nullable=True) # Optional due date, with timezone awareness
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Timestamp set by the DB on creation
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now()) # Timestamp updated by DB on modification

    # Foreign key relationship to the users table
    owner_id = Column(Integer, ForeignKey("users.id"))
    # Relationship to user: one task belongs to one user
    owner = relationship("User", back_populates="tasks")