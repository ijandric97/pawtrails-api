from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

from neotime import DateTime
from py2neo.ogm import Property, RelatedFrom
from pydantic import BaseModel as Schema

from app.core.database import BaseModel, BaseSchema

if TYPE_CHECKING:
    from app.models.user import User

energy: List[int] = [1, 2, 3, 4, 5]


class Pet(BaseModel):
    __primarykey__ = "uuid"

    name = Property(key="name")
    breed = Property(key="breed")
    _energy = Property(key="energy", default=3)
    _size = Property(key="size", default="Medium")

    _owners = RelatedFrom("app.models.user.User", "OWNS")

    @property
    def energy(self) -> Literal[1, 2, 3, 4, 5]:
        return self._energy

    @energy.setter
    def energy(self, energy: int) -> None:
        if not isinstance(energy, int):
            raise TypeError(f"Energy {energy} is not an integer.")
        if energy not in [1, 2, 3, 4, 5]:
            raise ValueError(f"Energy {energy} is not on scale [1-5].")
        self._energy = energy

    @property
    def size(self) -> Literal["Small", "Medium", "Big"]:
        return self._size

    @size.setter
    def size(self, size: str) -> None:
        if not isinstance(size, str):
            raise TypeError(f"Size {size} is not a string.")
        if size not in ["Small", "Medium", "Big"]:
            raise ValueError(f"Size {size} is not one of 'Small', 'Medium' or 'Big'")
        self._size = size

    @property
    def owners(self) -> List[User]:
        return [owner for owner in self._owners]

    def add_owner(self, user: User) -> bool:
        if user in self._owners:
            return False

        self._owners.add(user, created_at=DateTime.utc_now())
        self.save()

        return True

    def remove_owner(self, user: User) -> bool:
        if user not in self._owners:
            return False

        self._owners.remove(user)
        self.save()

        return True


class PetSchema(BaseSchema):
    name: str
    breed: str
    energy: Literal[1, 2, 3, 4, 5]
    size: Literal["Small", "Medium", "Big"]


class AddPetSchema(Schema):
    name: str
    breed: str
    energy: Literal[1, 2, 3, 4, 5]
    size: Literal["Small", "Medium", "Big"]


class Adder:
    pet_uuid: str
    user_uuid: str
