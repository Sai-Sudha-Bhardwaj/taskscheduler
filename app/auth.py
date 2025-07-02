# app/auth.py

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Import your crud, models, and schemas for type hinting and database interaction
from . import crud, models, schemas

# --- Configuration ---
# WARNING: CHANGE THIS SECRET KEY IN PRODUCTION! Use an environment variable.
SECRET_KEY = "super_secret_key_that_is_very_long_and_random_for_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # For example, 30 minutes

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

# --- Authentication & Token Functions ---

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """
    Authenticates a user by email and password.
    Returns the User object if authentication is successful, None otherwise.
    """
    user = crud.get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- OAuth2PasswordBearer Setup (used by dependency functions) ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Current User Dependency Functions for FastAPI Routes ---

async def get_current_user_from_token(
    db: Session,
    token: str, # This token is passed from the Depends(oauth2_scheme) in main.py
    credentials_exception: HTTPException # This exception object is passed from main.py
) -> models.User:
    """Decodes JWT token and retrieves user from DB."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    db: Session,
    token: str,
    credentials_exception: HTTPException
) -> models.User:
    """
    Retrieves the current active user based on the provided token.
    This is the function called directly in main.py's get_current_user wrapper.
    """
    user = await get_current_user_from_token(db, token, credentials_exception)
    if user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user