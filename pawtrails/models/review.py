from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, Optional

from neotime import DateTime
from py2neo.ogm import Property, RelatedFrom, RelatedTo
from pydantic import BaseModel as Schema

from pawtrails.core.database import BaseModel, BaseSchema, repository
from pawtrails.models.location import LocationSchema
from pawtrails.models.user import UserSchema
from pawtrails.utils import is_allowed_literal, override

if TYPE_CHECKING:
    from pawtrails.models.location import Location
    from pawtrails.models.user import User

AllowedReviewGrades = Literal[1, 2, 3, 4, 5]


class Review(BaseModel):
    comment = Property(key="grade", default="")
    _grade = Property(key="grade", default=3)

    _writer = RelatedFrom("pawtrails.models.user.User", "WROTE")
    _location = RelatedTo("pawtrails.models.location.Location", "FOR")

    @classmethod
    def get_by_grade(
        cls, grade: AllowedReviewGrades, skip: int = 0, limit: int = 100
    ) -> List[Review]:
        return [
            review
            for review in cls.match(repository)
            .where(grade=grade)
            .skip(skip)
            .limit(limit)
            .all()
        ]

    @property
    def grade(self) -> AllowedReviewGrades:
        return self._grade

    @grade.setter
    def grade(self, grade: int) -> None:
        if not isinstance(grade, int):
            raise TypeError(f"Grade {grade} is not an integer.")
        is_allowed_literal(grade, "Grade", AllowedReviewGrades)
        self._grade = grade

    @property
    def writer(self) -> User:
        return self._writer

    def add_writer(self, user: User) -> bool:
        if self._writer:
            return False
        self._writer.add(user, created_at=DateTime.utc_now())
        return True

    def remove_writer(self, user: User) -> bool:
        if user not in self._writer:
            return False
        self._writer.remove(user)
        return True

    @property
    def location(self) -> Location:
        return self._location

    def add_location(self, location: Location) -> bool:
        if self._location:
            return False
        self._location.add(location, created_at=DateTime.utc_now())
        return True

    def remove_location(self, location: Location) -> bool:
        if location not in self._location:
            return False
        self._location.remove(location)
        return True

    @override
    def save(self) -> None:
        if not self._writer:
            raise AttributeError("Cannot save Review: writer not defined.")
        if not self._location:
            raise AttributeError("Cannot save Review: location not defined.")
        if len(self._writer) > 1:
            raise AttributeError("Cannot save Review: more than 1 writer.")
        if len(self._location) > 1:
            raise AttributeError("Cannot save Review: more than 1 location.")
        super().save()


class ReviewSchema(BaseSchema):
    comment: str
    grade: AllowedReviewGrades


class FullReviewSchema(BaseSchema):
    writer: Optional[UserSchema]
    location: Optional[LocationSchema]


class AddReviewSchema(Schema):
    comment: str
    grade: AllowedReviewGrades


class UpdateReviewSchema(Schema):
    comment: Optional[str]
    grade: Optional[AllowedReviewGrades]
