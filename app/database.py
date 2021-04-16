"""
This is where we set up SQLAlchemy for later use
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, Integer

# TODO: Switch this to Postgres with docker
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# TODO: makni ovaj check same thread kad switchas na postgres, treba samo za sqlite to
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Svaka instanca ovoga ce biti sesija s bazom
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Ovo je common model
class Base(object):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# Iz ovog nasljedujemo ORM modele
Base = declarative_base(cls=Base)
