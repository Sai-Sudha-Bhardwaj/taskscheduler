# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

# Import your local modules
from . import crud, models, schemas, auth
from .database import engine, get_db

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, # Change to DEBUG for more verbose output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)
logger.info("Database tables checked/created.")

app = FastAPI()

# --- CORS Middleware ---
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173", # Allow your frontend to connect
    # Add other frontend URLs if deployed elsewhere
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allows all headers
)

# --- OAuth2 Scheme for token handling ---
# This is defined here because FastAPI's Depends uses it directly
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Dependency to get current user from token ---
# This function acts as a wrapper that calls the async function in auth.py
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Call the actual token parsing and user retrieval logic from auth.py
    user = await auth.get_current_active_user(db, token, credentials_exception)
    logger.debug(f"Current user: {user.email}")
    return user


# --- User Endpoints ---

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    logger.info(f"Attempting login for user: {form_data.username}")
    # Use the authenticate_user function from auth.py
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Login failed for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Use the create_access_token function from auth.py
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    logger.info(f"User {user.email} logged in successfully.")
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to register new user: {user.email}")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.warning(f"Registration failed: User with email {user.email} already exists.")
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = crud.create_user(db=db, user=user)
    logger.info(f"User {created_user.email} registered successfully with ID: {created_user.id}")
    return created_user

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    logger.debug(f"Fetching profile for user: {current_user.email}")
    return current_user

@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user_endpoint(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Attempting to update user ID {user_id} by {current_user.email}")

    if user_id != current_user.id:
        logger.warning(f"Unauthorized attempt to update user ID {user_id} by {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        logger.error(f"User ID {user_id} not found for update.")
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = crud.update_user(db=db, db_user=db_user, user_update=user_update)
    logger.info(f"User ID {user_id} updated successfully.")
    return updated_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"User {current_user.email} attempting to delete user ID: {user_id}")

    if user_id != current_user.id:
        logger.warning(f"Unauthorized attempt to delete user ID {user_id} by {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        logger.error(f"Deletion failed: User ID {user_id} not found.")
        raise HTTPException(status_code=404, detail="User not found")

    crud.delete_user(db, user_id=user_id)
    logger.info(f"User ID {user_id} ({db_user.email}) successfully deleted by {current_user.email}.")
    # For status_code=204, return nothing or a simple dictionary, FastAPI handles it.
    return


# --- Task Endpoints ---

@app.post("/tasks/", response_model=schemas.Task)
def create_task_for_current_user(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    logger.info(f"User {current_user.email} attempting to create task: {task.title}")
    created_task = crud.create_user_task(db=db, task=task, user_id=current_user.id)
    logger.info(f"Task '{created_task.title}' created by {current_user.email} with ID: {created_task.id}")
    return created_task

@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    logger.debug(f"User {current_user.email} fetching tasks (skip={skip}, limit={limit}).")
    tasks = crud.get_tasks(db, user_id=current_user.id, skip=skip, limit=limit)
    logger.info(f"User {current_user.email} fetched {len(tasks)} tasks.")
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    logger.debug(f"User {current_user.email} attempting to fetch task ID: {task_id}")
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None or db_task.owner_id != current_user.id:
        logger.warning(f"Task ID {task_id} not found or not owned by {current_user.email}")
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")
    logger.info(f"User {current_user.email} fetched task ID: {task_id}")
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task_endpoint(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    logger.info(f"User {current_user.email} attempting to update task ID: {task_id}")
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None or db_task.owner_id != current_user.id:
        logger.warning(f"Update failed: Task ID {task_id} not found or not owned by {current_user.email}")
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")

    updated_task = crud.update_task(db=db, db_task=db_task, task_update=task_update)
    logger.info(f"Task ID {task_id} updated successfully by {current_user.email}.")
    return updated_task

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    logger.info(f"User {current_user.email} attempting to delete task ID: {task_id}")
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None or db_task.owner_id != current_user.id:
        logger.warning(f"Delete failed: Task ID {task_id} not found or not owned by {current_user.email}")
        raise HTTPException(status_code=404, detail="Task not found or unauthorized")

    crud.delete_task(db=db, task_id=task_id)
    logger.info(f"Task ID {task_id} deleted successfully by {current_user.email}.")
    return db_task

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the Task Scheduler API!"}