from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from uuid import uuid4

import jsonpickle
from neotime import DateTime
from py2neo import Graph  # noqa
from py2neo.ogm import Model, Property, Repository
from pydantic import UUID4
from pydantic import BaseModel as Schema
from pydantic import Field

from pawtrails.core.settings import settings

graph = Graph(
    host=settings.NEO4J_HOST,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASS),
    name=settings.NEO4J_GRAPH_NAME,
)

repository = Repository(
    host=settings.NEO4J_HOST,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASS),
    name=settings.NEO4J_GRAPH_NAME,
)


class BaseModel(Model):
    """A Neo4j OGM Base Model. This class extends the base model with some useful
    methods. Additionaly contains automatic created and updated timestamp on save.
    """

    __primarykey__ = "uuid"

    _uuid = Property(key="uuid")
    _created_at = Property(key="created_at")
    _updated_at = Property(key="updated_at", default=DateTime.utc_now())

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a Neo4J Model

        Args:
            kwargs (dict): A list of fields to initialize with
        """
        self.update(**kwargs)

    @classmethod
    def get_by_uuid(cls, uuid: str) -> BaseModel:
        """Returns a node that matches the UUID4 hex string.

        Args:
            uuid (str): An UUID4 hex string

        Returns:
            BaseModel: Node with matching uuid
        """
        return cls.match(repository).where(uuid=uuid).first()

    @classmethod
    def get_all(cls, skip: int = 0, limit: int = 100) -> List[BaseModel]:
        """Returns all nodes of this Model from the database

        Returns:
            Optional[List[Model]]: List of Nodes with this Model type
        """
        return [model for model in cls.match(repository).skip(skip).limit(limit).all()]

    @property
    def uuid(self) -> Optional[str]:
        """Returns the UUID4 hex string that represents a unique id of this object.

        Returns:
            Optional[str]: UUID4 hex string
        """
        return self._uuid

    @property
    def created_at(self) -> Optional[datetime]:
        """Returns the date and time when the Node was created

        Returns:
            Optional[datetime]: DateTime when the Node was created
        """
        if self._created_at:
            return self._created_at.to_native()
        return None

    @property
    def updated_at(self) -> Optional[datetime]:
        """Returns the last date and time the object was updated

        Returns:
            Optional[datetime]: DateTime of the last Node update
        """
        if self._updated_at:
            return self._updated_at.to_native()
        return None

    def update(self, **kwargs: Any) -> None:
        """Updates a Neo4J Model with specified dict

        Args:
            kwargs (dict): A list of fields to update with
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def save(self) -> None:
        """Save the Neo4j Model Object"""
        if not self._uuid:
            self._uuid = uuid4().hex
        if not self._created_at:
            self._created_at = DateTime.utc_now()
        self._updated_at = DateTime.utc_now()
        repository.save(self)

    def delete(self) -> None:
        """Delete the Neo4j Model Object"""
        repository.delete(self)

    def to_json(self) -> str:
        """Returns a JSON representation of this object.

        Returns:
            str: JSON representation of this Neo4j Model
        """
        return jsonpickle.encode(self, unpicklable=False)


class BaseSchema(Schema):
    """A Pydantic schema model that matches the py2Neo OGM BaseModel described above.
    By default orm_mode is set to True."""

    uuid: Optional[UUID4] = Field(example="12345678-1234-1234-1234-123456789abc")
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
