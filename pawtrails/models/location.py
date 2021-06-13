from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

from neotime import DateTime
from py2neo.data.spatial import WGS84Point
from py2neo.ogm import Property, RelatedFrom, RelatedTo
from pydantic import BaseModel as Schema
from pydantic.fields import Field

from pawtrails.core.database import BaseModel, BaseSchema, graph
from pawtrails.models.constants import (
    AllowedLocationSizes,
    AllowedLocationTypes,
    AllowedReviewGrades,
)
from pawtrails.models.tag import TagSchema
from pawtrails.models.user import UserSchema
from pawtrails.utils import is_allowed_literal, override

if TYPE_CHECKING:
    from pawtrails.models.review import Review
    from pawtrails.models.tag import Tag
    from pawtrails.models.user import User


class Location(BaseModel):
    name = Property(key="name")
    description = Property(key="description", default="")
    _type = Property(key="type", default="park")
    _size = Property(key="size", default="medium")
    _location = Property(key="location")

    _creator = RelatedFrom("pawtrails.models.user.User", "CREATED")
    _tags = RelatedTo("pawtrails.models.tag.Tag", "TAGGED_AS")
    _favorites = RelatedFrom("pawtrails.models.user.User", "FAVORITED")
    _reviews = RelatedFrom("pawtrails.models.review.Review", "FOR")

    @classmethod
    def search(cls, params: SearchLocationOptions) -> List[Location]:
        query: str = (
            "MATCH (l:Location)"
            f'\nWHERE toLower(l.name) CONTAINS toLower("{params.name}")'
        )
        if params.size:
            query += f' AND l.size = "{params.size.lower()}"'
        if params.type:
            query += f' AND l.type = "{params.type.lower()}"'
        if params.user:
            query += (
                "\nWITH l"
                f'\nMATCH (u:User {{ uuid: "{params.user.uuid}" }})'
                "\nWITH u, l"
            )
            if params.user.created:
                query += "\nMATCH (u)-[:CREATED]->(l)"
            if params.user.favorited:
                query += "\nMATCH (u)-[:FAVORITED]->(l)"
        if params.grade:
            query += (
                "\nWITH l"
                "\nMATCH (l)<-[:FOR]-(r:Review)"
                "\nWITH l, avg(r.grade) AS grade"
                f"\nWHERE grade >= {params.grade}"
            )
        if params.distance:
            query += (
                f"\nWITH l, distance(point({{longitude: {params.distance.longitude},"
                f" latitude: {params.distance.latitude}}}), l.location)/1000 AS dist"
                f"\nWHERE dist <= {params.distance.max}"
            )
        query += f"\nRETURN l SKIP {params.skip} LIMIT {params.limit}"
        print(query, flush=True)

        locs: List[Location] = []
        for record in graph.run(query):
            locs.append(Location.wrap(record["l"]))

        return locs

    @property
    def type(self) -> AllowedLocationTypes:
        return self._type

    @type.setter
    def type(self, loc_type: str) -> None:
        if not isinstance(loc_type, str):
            raise TypeError(f"Type {loc_type} is not a string.")
        loc_type = loc_type.lower()
        is_allowed_literal(loc_type, "Type", AllowedLocationTypes)
        self._type = loc_type

    @property
    def size(self) -> AllowedLocationSizes:
        return self._size

    @size.setter
    def size(self, size: str) -> None:
        if not isinstance(size, str):
            raise TypeError(f"Size {size} is not a string.")
        size = size.lower()
        is_allowed_literal(size, "Size", AllowedLocationSizes)
        self._size = size

    @property
    def location(self) -> Dict[str, float]:
        if self._location:
            return {
                "longitude": self._location[0],
                "latitude": self._location[1],
            }
        return {}

    @location.setter
    def location(self, location_tuple: Tuple[float, float]) -> None:
        longitude, latitude = location_tuple
        if not isinstance(longitude, float):
            raise TypeError(f"Longitude {longitude} is not a float.")
        if not isinstance(latitude, float):
            raise TypeError(f"Latitude {latitude} is not a float.")
        self._location = WGS84Point((longitude, latitude))

    @property
    def creator(self) -> User:
        for creator in self._creator:
            return creator
        return self._creator  # This in reality is None but Mypy does not throw error :)

    def add_creator(self, user: User) -> bool:
        if self._creator:
            return False  # We already have a creator
        self._creator.add(user, created_at=DateTime.utc_now())
        return True

    def remove_creator(self, user: User) -> bool:
        if user not in self._creator:
            return False
        self._creator.remove(user)
        return True

    @property
    def tags(self) -> List[Tag]:
        return [tag for tag in self._tags]

    def add_tag(self, tag: Tag) -> bool:
        if tag in self._tags:
            return False
        self._tags.add(tag, created_at=DateTime.utc_now())
        return True

    def remove_tag(self, tag: Tag) -> bool:
        if tag not in self._tags:
            return False
        self._tags.remove(tag)
        return True

    @property
    def favorites(self) -> List[User]:
        return [favorite for favorite in self._favorites]

    def add_favorite(self, user: User) -> bool:
        if user in self._favorites:
            return False
        self._favorites.add(user, created_at=DateTime.utc_now())
        return True

    def remove_favorite(self, user: User) -> bool:
        if user not in self._favorites:
            return False
        self._favorites.add(user, created_at=DateTime.utc_now())
        return True

    @property
    def reviews(self) -> List[Review]:
        return [review for review in self._reviews]

    @property
    def grade(self) -> float:
        i = 0
        sum = 0
        for review in self._reviews:
            i += 1
            sum += review.grade
        if i <= 0 or sum <= 0:
            return 0
        return sum / i

    @override
    def save(self) -> None:
        if not self.name:
            raise AttributeError("Cannot save Location: name not defined.")
        if not self._location:
            raise AttributeError("Cannot save Location: location not defined.")
        if not self._creator:
            raise AttributeError("Cannot save Location: creator not defined.")
        if len(self._creator) > 1:
            raise AttributeError("Cannot save Location: more than 1 creator.")
        super().save()


class LocationSchema(BaseSchema):
    name: str
    description: str
    type: AllowedLocationTypes
    size: AllowedLocationSizes
    location: Dict[str, float] = Field(example="longitude, latitude")
    creator: UserSchema
    grade: float


class FullLocationSchema(LocationSchema):
    creator: UserSchema
    tags: Optional[List[TagSchema]]
    favorites: Optional[List[UserSchema]]


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
