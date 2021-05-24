from typing import Any, Dict, Generator

import pytest
from fastapi.testclient import TestClient

from pawtrails.main import app

bearer_token = ""
user_uuid = ""


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


def set_bearer(token: str) -> None:
    global bearer_token
    bearer_token = token


def bearer_header() -> Dict[str, Any]:
    global bearer_token
    return {"Authorization": f"Bearer {bearer_token}"}


def set_uuid(uuid: str) -> None:
    global user_uuid
    user_uuid = uuid


def get_uuid() -> str:
    global user_uuid
    return user_uuid
