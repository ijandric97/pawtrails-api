from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel as Schema
from pydantic import Field
from typing_extensions import Annotated

from pawtrails.models.base import BaseModel
from pawtrails.models.constants import AllowedPetEnergies, AllowedPetSizes

if TYPE_CHECKING:
    from pawtrails.models.user import User


class Pet(BaseModel):
    name: str
    breed: str
    energy: AllowedPetEnergies
    size: AllowedPetSizes
    owners: Optional[List[User]]


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
