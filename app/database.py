# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use a SQLite database for simplicity, replace with PostgreSQL/MySQL for production
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# For PostgreSQL: SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host/dbname"
# For MySQL: SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://user:password@host/dbname"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # Needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()