import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Using SQLite for now (file-based)
# SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"


# For PostgreSQL (future-ready):
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5433/user_db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine (SQLALCHEMY_DATABASE_URL)
                        # connect_args={"check_same_thread": False}  # Only for SQLite

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
