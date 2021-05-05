from __future__ import annotations

from typing import Optional

from py2neo.ogm import Property

from app.core.database import BaseModel, repository
from app.core.security import get_password_hash, verify_password


class User(BaseModel):
    __primarykey__ = "email"

    _email = Property(key="email")
    _username = Property(key="username")
    _password = Property(key="password")

    is_active = Property(key="is_active", default=True)

    @classmethod
    def get_by_email(cls, email: str) -> Optional[User]:
        return cls.match(repository, email).first()

    @classmethod
    def get_by_username(cls, username: str) -> Optional[User]:
        return cls.match(repository).where(username=username).first()

    @classmethod
    def authenticate(cls, email: str, password: str) -> Optional[User]:
        user = cls.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        self._email = email

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        self._username = username

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        self._password = get_password_hash(password)
