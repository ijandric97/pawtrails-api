from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from neo4j.spatial import WGS84Point
from pydantic import BaseModel as Schema
from pydantic import EmailStr
from pydantic.fields import Field
from typing_extensions import Annotated

from pawtrails.models.base import BaseModel
from pawtrails.models.pet import Pet


class User(BaseModel):
    password: Optional[str]
    email: Optional[EmailStr]
    username: Optional[str]
    full_name: Optional[str]
    is_active: Optional[bool] = True
    following_count: Optional[int]
    followers_count: Optional[int]
    home: Optional[WGS84Point]
    following: Optional[List[User]]
    # pets: Optional[List[Pet]]


# NOTE: THIS IS VERY IMPORTANT, OTHERWISE A SELF-REFERENCING MODEL WILL CRASH WITH A
# COMPLETELY RANDOM MESSAGE. SEE OFFICIAL PYDANTIC DOCS FOR MORE INFO:
# https://pydantic-docs.helpmanual.io/usage/postponed_annotations/#self-referencing-models
User.update_forward_refs()


class AddUserSchema(Schema):
    email: EmailStr = Field(example="user@example.com")
    username: Annotated[str, Field(example="user", min_length=3)]
    password: Annotated[str, Field(example="password", min_length=8)]


class UpdateUserSchema(Schema):
    email: Optional[EmailStr] = Field(example="user@example.com")
    username: Annotated[Optional[str], Field(example="user", min_length=3)]
    password: Annotated[Optional[str], Field(example="password", min_length=8)]
    old_password: Annotated[Optional[str], Field(example="password", min_length=8)]
    full_name: Optional[str]
    home_longitude: Optional[float]
    home_latitude: Optional[float]


class DashboardSchema(Schema):
    user: str = ""
    user_uuid: str = ""
    action: str = ""
    label: str = ""
    name: str = ""
    time: str = ""
    uuid: str = ""
