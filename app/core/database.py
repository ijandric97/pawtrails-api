from typing import TypeVar

import jsonpickle
from neotime import DateTime
from py2neo import Graph  # noqa
from py2neo.ogm import Model, Property, Repository

from app.core.settings import settings

ModelType = TypeVar("ModelType", bound=Model)

graph = Repository(
    host=settings.NEO4J_HOST,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
    name=settings.NEO4J_GRAPH_NAME,
)

repository = Repository(
    host=settings.NEO4J_HOST,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
    name=settings.NEO4J_GRAPH_NAME,
)


class BaseModel(Model):
    """A Neo4j OGM Base Model. This class extends the base model with some useful
    methods. Additionaly contains automatic created and updated timestamp on save.
    """

    _created_at = Property(key="created_at")
    _updated_at = Property(key="updated_at", default=DateTime.utc_now())

    def __init__(self: Model, **kwargs: dict) -> None:
        """Initialize a Neo4J Model

        Args:
            self (Model): Neo4j Model object
            kwargs (dict): A list of fields to initialize with
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def get_all(cls):
        return cls.match(repository)

    @property
    def created_at(self):
        if self._created_at:
            return self._created_at.to_native()
        return None

    @property
    def updated_at(self):
        if self._updated_at:
            return self._updated_at.to_native()
        return None

    def save(self) -> None:
        """Save the Neo4j Model Object"""
        if not self._created_at:
            self._created_at = DateTime.utc_now()
        self._updated_at = DateTime.utc_now()
        repository.save(self)

    def delete(self) -> None:
        """Delete the Neo4j Model Object"""
        repository.delete(self)

    def to_json(self: Model) -> str:
        """Returns a JSON representation of this object.

        Args:
            self (Model): Neo4j Model object

        Returns:
            str: JSON representation of this Neo4j Model
        """
        return jsonpickle.encode(self, unpicklable=False)
