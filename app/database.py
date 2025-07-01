# taskScheduler/app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Update the DATABASE_URL for SQLite
# This will create a file named 'sql_app.db' in the root of your project
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./sql_app.db"
)

# 2. Configure the engine for SQLite
# The 'connect_args' is crucial for SQLite with FastAPI/async operations
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} # <--- IMPORTANT for SQLite
)

# No change needed here
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# No change needed here
Base = declarative_base()

# Dependency to get a database session (no changes here)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()