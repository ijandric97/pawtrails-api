from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel as Schema
from pydantic.fields import Field

from pawtrails.models.base import BaseModel
from pawtrails.models.constants import (
    AllowedLocationSizes,
    AllowedLocationTypes,
    AllowedReviewGrades,
)
from pawtrails.models.tag import Tag
from pawtrails.models.user import User


class Location(BaseModel):
    name: str
    description: str
    type: AllowedLocationTypes
    size: AllowedLocationSizes
    location: Dict[str, float] = Field(example="longitude, latitude")
    grade: float
    creator: Optional[User]
    tags: Optional[List[Tag]]
    favorites: Optional[List[User]]


class AddLocationSchema(Schema):
    name: str
    description: str
    type: AllowedLocationTypes
    size: AllowedLocationSizes
    location: Tuple[float, float] = Field(example="45, 45")


class UpdateLocationSchema(Schema):
    name: Optional[str]
    description: Optional[str]
    type: Optional[AllowedLocationTypes]
    size: Optional[AllowedLocationSizes]
    location: Optional[Tuple[float, float]] = Field(example="45, 45")


class SearchLocationUserOptions(Schema):
    uuid: str
    created: bool
    favorited: bool


class SearchLocationDistanceOptions(Schema):
    longitude: float
    latitude: float
    max: float


class SearchLocationOptions(Schema):
    user: Optional[SearchLocationUserOptions]
    name: Optional[str] = ""
    size: Optional[AllowedLocationSizes]
    type: Optional[AllowedLocationTypes]
    grade: Optional[AllowedReviewGrades]
    distance: Optional[SearchLocationDistanceOptions]
    skip: Optional[int] = 0
    limit: Optional[int] = 100


class SearchLocationSchema(Schema):
    created: Optional[bool]
    favorited: Optional[bool]
    name: Optional[str] = ""
    size: Optional[AllowedLocationSizes]
    type: Optional[AllowedLocationTypes]
    grade: Optional[AllowedReviewGrades]
    longitude: Optional[float]
    latitude: Optional[float]
    max_distance: Optional[float]
    skip: Optional[int] = 0
    limit: Optional[int] = 100


class Point(Schema):
    longitude: float
    latitude: float
