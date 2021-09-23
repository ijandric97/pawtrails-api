import textwrap
from datetime import datetime
from typing import Optional, cast

from neo4j import (
    TRUST_ALL_CERTIFICATES,
    TRUST_SYSTEM_CA_SIGNED_CERTIFICATES,
    GraphDatabase,
    Neo4jDriver,
)
from neo4j.data import Record
from neo4j.time import DateTime

from pawtrails.database.base import BaseDatabase
from pawtrails.models.base import BaseModel
from pawtrails.models.user import User


class Neo4jDatabase(BaseDatabase):
    """
    A client for the Neo4j database.
    """

    _driver: Neo4jDriver = None

    def __init__(
        self,
        *,
        host: str,
        port: int,
        user: str = "neo4j",
        password: str = "test",
        encrypted: bool = False,
        validate_ssl: bool = False,
        max_connection_pool_size: int = 50,
        max_connection_lifetime: int = 100,
        **kwargs: dict,
    ) -> None:
        """Initialize a Neo4j database client.

        Args:
            host (str): Neo4j host URL
            port (int): Neo4j host port
            user (str, optional): Neo4j login username. Defaults to "neo4j".
            password (str, optional): Neo4j login password. Defaults to "test".
            encrypted (bool, optional): Neo4j login encryption. Defaults to False.
            validate_ssl (bool, optional): Should we validate this is a SSL connection.
                Defaults to False.
            max_connection_pool_size (int, optional): Maximal number of parallel
                conenctions to the Neo4j instance. Defaults to 50.
            max_connection_lifetime (int, optional): Maximum time (in seconds) a
                connection can stay alive . Defaults to 100.
        """
        self._driver = GraphDatabase.driver(
            uri=f"bolt://{host}:{port}",
            auth=(user, password),
            max_connection_pool_size=max_connection_pool_size,
            connection_timeout=10,
            max_connection_lifetime=max_connection_lifetime,
            encrypted=encrypted,
            trust=(
                TRUST_SYSTEM_CA_SIGNED_CERTIFICATES
                if validate_ssl
                else TRUST_ALL_CERTIFICATES
            ),
        )

    def _fix_temporal_types(self, record: Record) -> None:
        for attribute in record:
            if isinstance(record[attribute], DateTime):
                record._properties[attribute] = cast(
                    DateTime, record[attribute]
                ).to_native()

    def get_user(
        self,
        *,
        uuid: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Optional[User]:
        # Generate the query first
        query = "MATCH (user:User)\n"
        if uuid:
            query += f"WHERE user.uuid = '{uuid}'\n"
        elif username:
            query += f"WHERE user.username = '{username}'\n"
        elif email:
            query += f"WHERE user.email = '{email}'\n"
        else:
            raise ValueError("Neither uuid, username or email has been specified.")
        query += "RETURN user"

        # Execute the query
        with self._driver.session() as session:
            result = session.run(query)

            # Crash if we did not get a single result or we got more than one
            if not result:
                return None

            record = result.single()
            if not record:
                return None

            user = record["user"]

            self._fix_temporal_types(user)
            return User(**user)

    def create_user(self, *, user: User) -> Optional[User]:
        if not user.email or not user.password or not user.username:
            raise ValueError(
                "User object has to contain a valid email, username and password"
            )

        user.set_dates()

        query = textwrap.dedent(
            f"""
            CREATE (n:User)
            SET n.uuid = "{user.uuid}"
            SET n.created_at = "{user.created_at}"
            SET n.updated_at = "{user.updated_at}"
            SET n.password = "{user.password}"
            SET n.email = "{user.email}"
            SET n.username = "{user.username}"
            SET n.full_name = "{user.full_name}"
            SET n.is_active = {True}
            RETURN n as user
            """
        )

        print(query, flush=True)

        # Execute the query
        with self._driver.session() as session:
            result = session.run(query)

            # Crash if we did not get a single result or we got more than one
            if not result:
                return None

            record = result.single()
            if not record:
                return None

            user_ret = record["user"]

            # self._fix_temporal_types(user)
            return User(**user_ret)
