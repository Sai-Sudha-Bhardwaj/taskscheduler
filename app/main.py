# taskScheduler/app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List # Explicitly import List for type hints

from app import models, schemas, crud # Your application's components
from app.database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Create database tables if they don't exist
# This is typically run once during application startup in dev, or via migrations in production
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Allow your Vue.js frontend to communicate
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allow all headers
)

# Dependency to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db # Provide the session to the route handler
    finally:
        db.close() # Ensure the session is closed after the request is handled

# --- User Endpoints ---

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_200_OK)
def create_user_or_get_existing(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user if the username does not exist,
    otherwise returns the existing user.
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        # If user exists, return existing user
        return db_user
    # If user does not exist, create a new one
    return crud.create_user(db, user)

# --- Task Endpoints ---

@app.post("/users/{user_id}/tasks/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task_for_user(
    user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
):
    """
    Creates a new task associated with a specific user.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return crud.create_user_task(db=db, task=task, user_id=user_id)

@app.get("/users/{user_id}/tasks", response_model=List[schemas.Task])
def read_user_tasks(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all tasks for a specific user.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return crud.get_user_tasks(db, user_id=user_id)

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing task by its ID.
    Supports partial updates (only send fields you want to change).
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return crud.update_task(db=db, task_id=task_id, task_update=task_update)

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Deletes a task by its ID.
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    crud.delete_task(db=db, task_id=task_id)
    # For a 204 No Content response, typically you don't return a body.
    # FastAPI will handle this correctly; returning a dictionary is fine,
    # but not strictly necessary for a 204.
    return {"message": "Task deleted successfully"}