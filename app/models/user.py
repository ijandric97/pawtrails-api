from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from neotime import DateTime
from py2neo.ogm import Property, RelatedFrom, RelatedTo
from pydantic import BaseModel as Schema
from pydantic import EmailStr
from pydantic.fields import Field
from typing_extensions import Annotated

from app.core.database import BaseModel, BaseSchema, repository
from app.core.security import get_password_hash, verify_password

if TYPE_CHECKING:
    from app.models.pet import Pet


class User(BaseModel):
    __primarykey__ = "email"

    # TODO: Actually set this to false until user activates with mail
    # TODO: email on registering, use AWS for that
    is_active = Property(key="is_active", default=True)
    _email = Property(key="email")
    _username = Property(key="username")
    _password = Property(key="password")

    _following = RelatedTo("User", "FOLLOWS")
    _followers = RelatedFrom("User", "FOLLOWS")
    # NOTE: Import this whole things so there is not CIRCULAR IMPORTS
    _pets = RelatedTo("app.models.pet.Pet", "OWNS")

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
            raise TypeError(f"Email {email} is not an email.")
        if User.get_by_email(email):
            raise ValueError(f"Email {email} already exists.")
        self._email = email

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        if not isinstance(username, str):
            raise TypeError(f"Username {username} is not a string.")
        if User.get_by_username(username):
            raise ValueError(f"Username {username} already exists.")
        self._username = username

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        if not isinstance(password, str):
            raise TypeError(f"Password {password} is not a string.")
        self._password = get_password_hash(password)

    @property
    def following(self) -> List[User]:
        return [follow for follow in self._following]

    @property
    def followers(self) -> List[User]:
        return [follow for follow in self._followers]

    @property
    def pets(self) -> List[Pet]:
        return [pet for pet in self._pets]

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
    # following: Optional[List[UserSchema]]
    # pets: Optional[List[PetSchema]]


class RegisterUserSchema(Schema):
    email: EmailStr = Field(example="user@example.com")
    username: Annotated[str, Field(example="user", min_length=3)]
    password: Annotated[str, Field(example="password", min_length=8)]


class UpdateUserSchema(Schema):
    email: Optional[EmailStr] = Field(example="user@example.com")
    username: Annotated[Optional[str], Field(example="user", min_length=3)]
    password: Annotated[Optional[str], Field(example="password", min_length=8)]
