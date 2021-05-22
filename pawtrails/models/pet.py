from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, Optional

from neotime import DateTime
from py2neo.ogm import Property, RelatedFrom
from pydantic import BaseModel as Schema
from pydantic import Field
from typing_extensions import Annotated

from pawtrails.core.database import BaseModel, BaseSchema, repository
from pawtrails.utils import is_allowed_literal, override

if TYPE_CHECKING:
    from pawtrails.models.user import User

AllowedPetEnergies = Literal[1, 2, 3, 4, 5]
AllowedPetSizes = Literal["small", "medium", "big"]


class Pet(BaseModel):
    name = Property(key="name")
    breed = Property(key="breed")
    _energy = Property(key="energy", default=3)
    _size = Property(key="size", default="Medium")

    _owners = RelatedFrom("pawtrails.models.user.User", "OWNS")

    @classmethod
    def get_by_name(cls, name: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        return [
            pet
            for pet in cls.match(repository)
            .where(name=name)
            .skip(skip)
            .limit(limit)
            .all()
        ]

    @classmethod
    def get_by_breed(cls, breed: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        return [
            pet
            for pet in cls.match(repository)
            .where(breed=breed)
            .skip(skip)
            .limit(limit)
            .all()
        ]

    @classmethod
    def get_by_energy(
        cls, energy: AllowedPetEnergies, skip: int = 0, limit: int = 100
    ) -> List[Pet]:
        return [
            pet
            for pet in cls.match(repository)
            .where(energy=energy)
            .skip(skip)
            .limit(limit)
            .all()
        ]

    @classmethod
    def get_by_size(
        cls, size: AllowedPetSizes, skip: int = 0, limit: int = 100
    ) -> List[Pet]:
        return [
            pet
            for pet in cls.match(repository)
            .where(size=size)
            .skip(skip)
            .limit(limit)
            .all()
        ]

    @property
    def energy(self) -> AllowedPetEnergies:
        return self._energy

    @energy.setter
    def energy(self, energy: int) -> None:
        if not isinstance(energy, int):
            raise TypeError(f"Energy {energy} is not an integer.")
        is_allowed_literal(energy, "Energy", AllowedPetEnergies)
        self._energy = energy

    @property
    def size(self) -> AllowedPetSizes:
        return self._size

    @size.setter
    def size(self, size: str) -> None:
        if not isinstance(size, str):
            raise TypeError(f"Size {size} is not a string.")
        is_allowed_literal(size, "Size", AllowedPetSizes)
        self._size = size

    @property
    def owners(self) -> List[User]:
        return [owner for owner in self._owners]

    def add_owner(self, user: User) -> bool:
        if user in self._owners:
            return False
        self._owners.add(user, created_at=DateTime.utc_now())
        return True

    def remove_owner(self, user: User) -> bool:
        if user not in self._owners:
            return False
        self._owners.remove(user)
        return True

    @override
    def save(self) -> None:
        if not self._owners:
            raise AttributeError("Cannot save Pet: at least 1 owner is not defined.")
        super().save()


class PetSchema(BaseSchema):
    name: str
    breed: str
    energy: AllowedPetEnergies
    size: AllowedPetSizes


# TODO: Full pet schema, including owners :)


class AddPetSchema(Schema):
    name: Annotated[str, Field(example="Doge", min_length=1)]
    breed: Annotated[str, Field(example="Shiba Inu", min_length=1)]
    energy: AllowedPetEnergies
    size: AllowedPetSizes


class UpdatePetSchema(Schema):
    name: Annotated[Optional[str], Field(example="Doge", min_length=1)]
    breed: Annotated[Optional[str], Field(example="Shiba Inu", min_length=1)]
    energy: Optional[AllowedPetEnergies]
    size: Optional[AllowedPetSizes]


# TODO: Add save checks for name, breed, energy and size, they all have to be set !!!
