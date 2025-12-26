import os
import urllib
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

# Database configuration
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = urllib.parse.quote_plus(os.getenv('DB_PASSWORD')) if os.getenv('DB_PASSWORD') else ""
DB_NAME = os.getenv('DB_NAME')


if not all([DB_HOST, DB_PORT, DB_USER, DB_NAME]):
    raise ValueError("Database configuration is incomplete")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine with extended logging
try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        echo=False
    )
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
except Exception as e:
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        yield db
    except SQLAlchemyError as e:
        if "Access denied" in str(e):
            raise HTTPException(status_code=500, detail="Database authentication failed")
        elif "Unknown database" in str(e):
            raise HTTPException(status_code=500, detail="Database does not exist")
        elif "Can't connect" in str(e) or "Connection refused" in str(e):
            raise HTTPException(status_code=500, detail="Cannot connect to database server")
        else:
            raise HTTPException(status_code=500, detail=f"Database Connection Failed: {str(e)}")
    finally:
        db.close()
