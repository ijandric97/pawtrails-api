from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as Schema

from pawtrails.models.base import BaseModel
from pawtrails.models.constants import AllowedReviewGrades

if TYPE_CHECKING:
    from pawtrails.models.location import Location
    from pawtrails.models.user import User


class Review(BaseModel):
    comment: str
    grade: AllowedReviewGrades
    writer: Optional[User]
    location: Optional[Location]


class AddReviewSchema(Schema):
    comment: str
    grade: AllowedReviewGrades


class UpdateReviewSchema(Schema):
    comment: Optional[str]
    grade: Optional[AllowedReviewGrades]
