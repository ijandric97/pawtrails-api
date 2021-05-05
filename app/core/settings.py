import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


# TODO: Connect this with .env file, check Pydantic documentation
class Settings(BaseSettings):
    API_PREFIX: str = "/api/v0"  # This is the API prefix for version 0

    # JWT STUFF
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # This means 1 day
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl

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

    PROJECT_NAME: str = "PawTrails"

    # Neo4j
    NEO4J_HOST: str = "pawtrails_neo4j"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "test"
    NEO4J_GRAPH_NAME: str = "pawtrails"

    class Config:
        case_sensitive = True


settings = Settings()
