from sqlalchemy import Boolean, Column, String

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)

    # items = relationship("Item", back_populates="owner")
