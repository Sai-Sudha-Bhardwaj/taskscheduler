# taskScheduler/app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas # Import your models and schemas

# --- User CRUD Operations ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # Refresh to get auto-generated ID
    return db_user

# --- Task CRUD Operations ---
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_user_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # Filter tasks by owner_id
    return db.query(models.Task).filter(models.Task.owner_id == user_id).offset(skip).limit(limit).all()

def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    # Use task.model_dump() for Pydantic v2 to convert schema to dictionary
    # exclude_unset=True ensures only provided fields are included, good for Optional fields
    db_task = models.Task(**task.model_dump(exclude_unset=True), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task) # Refresh to get auto-generated ID, created_at, updated_at
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        # Convert Pydantic schema to dictionary, excluding fields that were not set by the client
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value) # Dynamically set attributes on the SQLAlchemy model instance
        db.add(db_task) # Add the modified object back to the session
        db.commit() # Commit changes to the database
        db.refresh(db_task) # Refresh to get the latest state, including updated_at
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task # Return the deleted object (or None if not found initially)