import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models.models import table_registry    # NoQA
from services.settings import Settings  # NoQA


engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine, expire_on_commit=False) as session:
        yield session

def create_db():
    try:
        table_registry.metadata.create_all(engine)
        logging.info("Database tables created successfully.")
    except Exception as e:
        logging.error(f"Failed to create database tables: {e}")
        raise
