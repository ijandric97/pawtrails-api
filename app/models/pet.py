from __future__ import annotations

from typing import List, Literal

from py2neo.ogm import Property, RelatedFrom

from app.core.database import BaseModel
from app.models.user import User

energy: List[int] = [1, 2, 3, 4, 5]


class Pet(BaseModel):
    __primarykey__ = "uuid"

    name = Property(key="name")
    breed = Property(key="breed")
    _energy = Property(key="energy", default=3)
    _size = Property(key="size", default="Medium")

    _owners = RelatedFrom("User", "OWN")

    @property
    def energy(self) -> Literal[1, 2, 3, 4, 5]:
        return self._energy

    @energy.setter
    def energy(self, energy: int) -> bool:
        if energy not in [1, 2, 3, 4, 5]:
            return False
        self._energy = energy
        return True

    @property
    def size(self) -> Literal["Small", "Medium", "Big"]:
        return self._size

    @size.setter
    def size(self, size: str) -> bool:
        if size not in ["Small", "Medium", "Big"]:
            return False
        self._size = size
        return True

    @property
    def owners(self) -> List[User]:
        ret: List[User] = []

        for owner in self._owners:
            ret.append(owner)

        return ret
