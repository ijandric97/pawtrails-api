from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

from neotime import DateTime
from py2neo.ogm import Property, RelatedFrom, RelatedTo

from pawtrails.core.database import BaseModel, BaseSchema
from pawtrails.utils import is_allowed_literal

if TYPE_CHECKING:
    from pawtrails.models.tag import Tag
    from pawtrails.models.user import User

AllowedLocationTypes = Literal["park", "field"]
AllowedLocationSizes = Literal["small", "medium", "big"]


class Location(BaseModel):
    name = Property(key="name")
    description = Property(key="description")
    _type = Property(key="type")
    _size = Property(key="size")
    _location = Property(key="location")

    _creator = RelatedFrom("pawtrails.models.user.User", "CREATED")
    _tags = RelatedTo("pawtrails.models.tag.Tag", "TAGGED_AS")
    _favorites = RelatedFrom("pawtrails.models.user.User", "FAVORITED")

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


class LocationSchema(BaseSchema):
    name: str
    description: str
    type: AllowedLocationTypes
    size: AllowedLocationSizes
    location: str  # TODO: Not really, should be WGS84 a.k.a. py2neo spatial type...


# TODO: Add WGS84 location inside :)
# TODO: Add save checking
