from fastapi.testclient import TestClient

from pawtrails.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() is None
