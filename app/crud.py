# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas
from . import auth # Import auth for password hashing

# --- User CRUD Operations ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # Hash the password before storing it
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: models.User, user_update: schemas.UserUpdate):
    # Update fields only if they are provided in the update schema
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.password is not None:
        db_user.hashed_password = auth.get_password_hash(user_update.password) # Rehash new password
    if user_update.is_active is not None:
        db_user.is_active = user_update.is_active

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user # Returns the deleted object or None


# --- Task CRUD Operations ---
def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.model_dump(), owner_id=user_id) # Use model_dump() for Pydantic v2+
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, db_task: models.Task, task_update: schemas.TaskUpdate):
    # Update fields only if they are provided
    for key, value in task_update.model_dump(exclude_unset=True).items(): # Use exclude_unset=True to only update provided fields
        setattr(db_task, key, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task # Returns the deleted object or None