from __future__ import annotations

from pydantic import BaseModel as Schema
from pydantic.fields import Field
from typing_extensions import Annotated

from pawtrails.models.base import BaseModel
from pawtrails.models.constants import AllowedTagColors


class Tag(BaseModel):
    name: str
    color: AllowedTagColors


class AddTagSchema(Schema):
    name: Annotated[str, Field(example="Important", min_length=3)]
    color: AllowedTagColors
