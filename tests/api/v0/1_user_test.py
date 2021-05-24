from fastapi.testclient import TestClient

from pawtrails.core.settings import settings
from tests.conftest import bearer_header, get_uuid

TEST_USERNAME = "pytest_changed"


class TestGetMyUser:
    def test_no_token(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/")
        assert response.status_code == 401

    def test_success(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/", headers=bearer_header())
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["uuid"] == get_uuid()


class TestDeleteUser:
    def test_no_token(self, client: TestClient) -> None:
        response = client.delete(f"{settings.API_PREFIX}/user/")
        assert response.status_code == 401


class TestUpdateUser:
    def test_no_token(self, client: TestClient) -> None:
        response = client.patch(f"{settings.API_PREFIX}/user/")
        assert response.status_code == 401

    def test_invalid_params(self, client: TestClient) -> None:
        response = client.patch(f"{settings.API_PREFIX}/user/", headers=bearer_header())
        assert response.status_code == 422

    def test_success(self, client: TestClient) -> None:
        patch_data = {
            "username": TEST_USERNAME,
        }
        response = client.patch(
            f"{settings.API_PREFIX}/user/", headers=bearer_header(), json=patch_data
        )
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["username"] == TEST_USERNAME


class TestGetUserByUUID:
    def test_invalid_user(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/gibberish_user_wont_exist")
        assert response.status_code == 404

    def test_success(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/{get_uuid()}")
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["username"] == TEST_USERNAME


class TestGetFollowersByUUID:
    def test_invalid_user(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/user/gibberish_user_wont_exist/followers"
        )
        assert response.status_code == 404

    def test_success(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/{get_uuid()}/followers")
        response_json = response.json()
        assert response.status_code == 200
        assert response_json == []


class TestGetFollowingByUUID:
    def test_invalid_user(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/user/gibberish_user_wont_exist/following"
        )
        assert response.status_code == 404

    def test_success(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/{get_uuid()}/following")
        response_json = response.json()
        assert response.status_code == 200
        assert response_json == []


class TestGetPetsByUUID:
    def test_invalid_user(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/user/gibberish_user_wont_exist/pets"
        )
        assert response.status_code == 404

    def test_success(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/{get_uuid()}/pets")
        response_json = response.json()
        assert response.status_code == 200
        assert response_json == []
