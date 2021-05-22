from __future__ import annotations

from typing import Literal

from py2neo.ogm import Property

from pawtrails.core.database import BaseModel, BaseSchema
from pawtrails.utils import is_allowed_literal

AllowedTagColors = Literal[
    "primary", "secondary", "success", "danger", "warning", "info", "light", "dark"
]


class Tag(BaseModel):
    """Tag can be connected to other models, and be searched upon. It does not know of
    any relations; this is intentional. Tags should be connected to, created, deleted
    from other models.
    """

    name = Property(key="name")
    _color = Property(key="color")

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


class LocationSchema(BaseSchema):
    pass
