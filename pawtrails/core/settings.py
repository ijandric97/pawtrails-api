import secrets
from typing import List, Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, validator

DB_CLIENTS = {"NEO4J": "pawtrails.database.neo4j.Neo4jDatabase"}
"""A list of the available database clients."""


class Settings(BaseSettings):
    """
    A class which contains all the ENV variables properly converted and handled by
    underlying Pydantic BaseSettings class.
    """

    # Project RELATED
    APP_TITLE: str = "PawTrails"
    APP_DESCRIPTION: str = "A Web API for the PawTrails Application"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v0"  # This is the API prefix for version 0

    # JWT STUFF
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # This means 1 day
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)

    # DATABASE
    DB_HOST: str = "pawtrails_neo4j"
    DB_PORT: str = "7687"
    DB_USER: str = "neo4j"
    DB_PASSWORD: str = "test"
    DB_ENCRYPTED: bool = False
    DB_VALIDATE_SSL: bool = False
    DB_CLIENT: str = DB_CLIENTS["NEO4J"]
    DB_CLIENT_KWARGS: dict = {}

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


load_dotenv(".env")  # Load settings from the .env files
settings = Settings()  # Create a new instance of settings, this should be included
