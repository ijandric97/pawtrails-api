from typing import Generator

import pytest
from fastapi.testclient import TestClient

from pawtrails.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
