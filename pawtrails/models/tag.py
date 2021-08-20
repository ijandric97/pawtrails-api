from __future__ import annotations

from typing import List, Optional

from py2neo.ogm import Property
from pydantic import BaseModel as Schema
from pydantic.fields import Field
from typing_extensions import Annotated

from pawtrails.core.database import BaseModel, BaseSchema, repository
from pawtrails.models.constants import AllowedTagColors
from pawtrails.utils import is_allowed_literal


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

    @classmethod
    def get_by_color(
        cls, color: AllowedTagColors, skip: int = 0, limit: int = 100
    ) -> List[Tag]:
        return [
            tag
            for tag in cls.match(repository)
            .where(color=color)
            .skip(skip)
            .limit(limit)
            .all()
        ]

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


class AddTagSchema(Schema):
    name: Annotated[str, Field(example="Important", min_length=3)]
    color: AllowedTagColors
