# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://jobuser:jobpass@localhost:5432/jobboard')

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# helper for dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()