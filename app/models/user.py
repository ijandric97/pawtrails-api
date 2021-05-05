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
    def get_by_email(cls, email: str):
        return cls.match(repository, email).first()

    @classmethod
    def get_by_username(cls, username: str):
        return cls.match(repository).where(username=username).first()

    @classmethod
    def authenticate(cls, email: str, password: str):
        user = cls.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.get_password()):
            return None
        return user

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username: str):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = get_password_hash(password)
