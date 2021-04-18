"""
This is where we set up SQLAlchemy for later use
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, Integer

user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
db = os.environ.get("POSTGRES_DB")

# SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Svaka instanca ovoga ce biti sesija s bazom
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Ovo je common model
class Base(object):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )


# Iz ovog nasljedujemo ORM modele
Base = declarative_base(cls=Base)
