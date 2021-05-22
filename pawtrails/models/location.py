from __future__ import annotations

from typing import Literal

from py2neo.ogm import Property, RelatedFrom

from pawtrails.core.database import BaseModel, BaseSchema
from pawtrails.models.user import User
from pawtrails.utils import is_allowed_literal

AllowedLocationTypes = Literal["park", "field"]
AllowedLocationSizes = Literal["small", "medium", "big"]


class Location(BaseModel):
    name = Property(key="name")
    description = Property(key="description")
    _type = Property(key="type")
    _size = Property(key="size")
    _location = Property(key="location")

    _creator = RelatedFrom("pawtrails.models.user.User", "CREATED")

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

    # TODO: Zapisivanje creatora kod saveanja, po meni bi trebalo overrideat default
    # save funkciju


class LocationSchema(BaseSchema):
    pass
