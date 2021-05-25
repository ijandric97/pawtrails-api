from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Tuple

from neotime import DateTime
from py2neo.data.spatial import WGS84Point
from py2neo.ogm import Property, RelatedFrom, RelatedTo
from pydantic import BaseModel as Schema

from pawtrails.core.database import BaseModel, BaseSchema
from pawtrails.models.tag import TagSchema
from pawtrails.models.user import UserSchema
from pawtrails.utils import is_allowed_literal, override

if TYPE_CHECKING:
    from pawtrails.models.review import Review
    from pawtrails.models.tag import Tag
    from pawtrails.models.user import User

AllowedLocationTypes = Literal["park", "field"]
AllowedLocationSizes = Literal["small", "medium", "big"]


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
            print(self._location, flush=True)
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
        return self._creator

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
        return self._tags

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
        return self._favorites

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
        return self._reviews

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
    location: Dict[str, float]


class FullLocationSchema(LocationSchema):
    creator: UserSchema
    tags: Optional[List[TagSchema]]
    favorites: Optional[List[UserSchema]]


class AddLocationSchema(Schema):
    name: str
    description: str
    type: AllowedLocationTypes
    size: AllowedLocationSizes
    position: Tuple[float, float]


class UpdateLocationSchema(Schema):
    name: Optional[str]
    description: Optional[str]
    type: Optional[AllowedLocationTypes]
    size: Optional[AllowedLocationSizes]
    position: Optional[Tuple[float, float]]
