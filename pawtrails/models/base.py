from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import uuid4

import jsonpickle
from pydantic import BaseModel as Schema
from pydantic import Field


class BaseModel(Schema):
    """A Pydantic schema model that serves as a main entity model every subsequent model
    should derive from. This way every entity should have an UUID, and timestamps.
    The handling logic should be resolved by the database client.
    By default orm_mode is set to True."""

    uuid: Optional[str] = Field(example="12345678123412341234123456789abc")
    """A unique ID of this record."""

    created_at: Optional[datetime]
    """Date and time this record was created at."""

    updated_at: Optional[datetime]
    """Date and time this record was last updated at."""

    def to_json(self) -> str:
        """Returns a JSON representation of this object.

        Returns:
            str: JSON representation of this Neo4j Model
        """
        return jsonpickle.encode(self, unpicklable=False)

    def set_dates(self) -> None:
        """Sets created_at and updated_at to current date and time.

        Created_at is only set if it has not been previously set.
        """
        if not self.uuid:
            self.uuid = uuid4().hex
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

    class Config:  # Pydantic BaseModel config
        orm_mode = True
