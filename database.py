"""
Database setup for VCPnet Config Tool
"""

from sqlmodel import SQLModel, create_engine

# Import all models to ensure they're registered with SQLModel
from models import *

# SQLite database file
DATABASE_URL = "sqlite:///./vcpnet.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)