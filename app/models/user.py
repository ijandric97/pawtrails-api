from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from neotime import DateTime
from py2neo.ogm import Property, RelatedFrom, RelatedTo
from pydantic import BaseModel as Schema
from pydantic import EmailStr
from pydantic.fields import Field

from app.core.database import BaseModel, BaseSchema, repository
from app.core.security import get_password_hash, verify_password


class User(BaseModel):
    __primarykey__ = "email"

    _email = Property(key="email")
    _username = Property(key="username")
    _password = Property(key="password")
    is_active = Property(key="is_active", default=True)
    # TODO: Actually set this to false until user activates with mail
    # TODO: email on registering, use AWS for that

    _following = RelatedTo("User", "FOLLOW")
    _followers = RelatedFrom("User", "FOLLOW")

    @classmethod
    def get_all(cls, skip: int, limit: int) -> List[User]:  # type: ignore
        ret: List[User] = []

        for user in super().get_all(skip=skip, limit=limit):
            ret.append(user)

        return ret

    @classmethod
    def get_by_email(cls, email: str) -> Optional[User]:
        return cls.match(repository, email).first()

    @classmethod
    def get_by_username(cls, username: str) -> Optional[User]:
        return cls.match(repository).where(username=username).first()

    @classmethod
    def authenticate(cls, email: str, password: str) -> Optional[User]:
        user = cls.get_by_email(email=email)
        if not user or not verify_password(password, user.password):
            return None
        return user

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        if not isinstance(email, str):
            raise TypeError(f"{email} is not an email.")
        if User.get_by_email(email):
            raise ValueError(f"{email} already exists.")
        self._email = email

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        if not isinstance(username, str):
            raise TypeError(f"{username} is not a string.")
        if User.get_by_username(username):
            raise ValueError(f"{username} already exists.")
        self._username = username

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        if not isinstance(password, str):
            raise TypeError(f"{password} is not a string.")
        self._password = get_password_hash(password)

    @property
    def following(self) -> List[User]:
        ret: List[User] = []

        for follow in self._following:
            ret.append(follow)

        return ret

    @property
    def followers(self) -> List[User]:
        ret: List[User] = []

        for follow in self._followers:
            ret.append(follow)

        return ret

    def follow(self, user: User) -> bool:
        if self == user or user in self._following:
            return False

        self._following.add(user, created_at=DateTime.utc_now())
        self.save()  # NOTE: Saving is fine in methods, but not in properties

        return True

    def unfollow(self, user: User) -> bool:
        if self == user or user not in self._following:
            return False

        self._following.remove(user)
        self.save()

        return True


class UserSchema(BaseSchema):
    username: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    is_active: Optional[bool] = True


class UserFullSchema(UserSchema):
    email: Optional[EmailStr]


class RegisterUserSchema(Schema):
    email: EmailStr = Field(example="user@example.com")
    username: str = Field(example="user")
    password: str = Field(example="password")
