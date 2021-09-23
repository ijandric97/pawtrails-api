from threading import Lock

from pydantic.utils import import_string

from pawtrails.core.settings import settings
from pawtrails.database.base import BaseDatabase

_db_client = None
_db_client_lock = Lock()


def get_db_client() -> BaseDatabase:
    """A singleton pattern that returns an instance of the database client specified in
    the settings (environment variables).

    [extended_summary]

    Returns:
        BaseDatabase: An instance of the database client, as specified in the settings.
    """

    global _db_client

    if _db_client:
        return _db_client

    with _db_client_lock:
        if _db_client:
            return _db_client
        else:
            # Gather all the configuration to create a database client
            host = settings.DB_HOST
            port = settings.DB_PORT
            user = settings.DB_USER
            password = settings.DB_PASSWORD
            encrypted = settings.DB_ENCRYPTED
            validate_ssl = settings.DB_VALIDATE_SSL

            client_kwargs = settings.DB_CLIENT_KWARGS

            client = import_string(settings.DB_CLIENT)
            _db_client = client(
                host=host,
                port=port,
                user=user,
                password=password,
                encrypted=encrypted,
                validate_ssl=validate_ssl,
                client_kwargs=client_kwargs,
            )

    return _db_client
