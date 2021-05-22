from __future__ import annotations

from typing import Literal, Optional

from py2neo.ogm import Property

from pawtrails.core.database import BaseModel, BaseSchema, repository
from pawtrails.utils import is_allowed_literal

AllowedTagColors = Literal[
    "primary", "secondary", "success", "danger", "warning", "info", "light", "dark"
]


class Tag(BaseModel):
    """Tag can be connected to other models, and be searched upon. It does not know of
    any relations; this is intentional. Tags should be connected to, created, deleted
    from other models.
    """

    __primarykey__ = "name"  # This will prevent duplicates

    _name = Property(key="name")
    _color = Property(key="color", default="primary")

    @classmethod
    def get_by_name(cls, name: str) -> Optional[Tag]:
        return cls.match(repository).where(name=name).first()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError(f"Name {name} is not a string.")
        if len(name) < 3:
            raise ValueError(f"Name {name} is not at least 3 characters long.")
        self._name = name

    @property
    def color(self) -> AllowedTagColors:
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        if not isinstance(color, str):
            raise TypeError(f"Color {color} is not a string.")
        color = color.lower()
        is_allowed_literal(color, "Color", AllowedTagColors)
        self._color = color

    def save(self) -> None:
        if not self.name:
            raise AttributeError("Cannot save Tag: name not defined.")
        if Tag.get_by_name(self.name):
            raise RuntimeError(f"Cannot save Tag: {self.name} already exists.")
        super().save()


class TagSchema(BaseSchema):
    name: str
    colr: AllowedTagColors
