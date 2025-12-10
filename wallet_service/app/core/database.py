from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.core.connection import mongo_connect_with_retry, pg_connect_with_retry
import logging

load_dotenv()

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def postgres_db():
    """Dependency to get DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db_connections():
    """Initialize database connections"""
    try:
        global pg_connection, mongo_db
        pg_connection = pg_connect_with_retry()
        mongo_db = mongo_connect_with_retry()
        logger.info("Database connections established successfully")
    except Exception as e:
        logger.critical(f"Failed to establish database connections: {e}")
        raise e
