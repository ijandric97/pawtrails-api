from fastapi.testclient import TestClient

from pawtrails.core.settings import settings
from tests.conftest import set_bearer, set_uuid

TEST_EMAIL = "pytest@example.com"
TEST_USERNAME = "pytest"
TEST_PASSWORD = "password"


class TestRegister:
    def test_invalid_parameters(self, client: TestClient) -> None:
        response = client.post(f"{settings.API_PREFIX}/register", json=None)
        assert response.status_code == 422

    def test_success(self, client: TestClient) -> None:
        reg_data = {
            "email": TEST_EMAIL,
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
        }
        response = client.post(f"{settings.API_PREFIX}/register", json=reg_data)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["username"] == TEST_USERNAME
        set_uuid(response_json["uuid"])

    def test_already_exists(self, client: TestClient) -> None:
        reg_data = {
            "email": TEST_EMAIL,
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
        }
        response = client.post(f"{settings.API_PREFIX}/register", json=reg_data)
        assert response.status_code == 409


class TestLogin:
    def test_invalid_parameters(self, client: TestClient) -> None:
        response = client.post(f"{settings.API_PREFIX}/login", json=None)
        assert response.status_code == 422

    def test_wrong_auth_info(self, client: TestClient) -> None:
        login_data = {
            "username": TEST_EMAIL,
            "password": "any invalid password will do for this test",
        }
        response = client.post(f"{settings.API_PREFIX}/login", data=login_data)
        assert response.status_code == 401

    def test_success(self, client: TestClient) -> None:
        global bearer_token
        login_data = {"username": TEST_EMAIL, "password": TEST_PASSWORD}
        response = client.post(f"{settings.API_PREFIX}/login", data=login_data)
        response_json = response.json()
        set_bearer(response_json["access_token"])
        assert response.status_code == 200
