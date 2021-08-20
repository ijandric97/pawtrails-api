from fastapi.testclient import TestClient

from pawtrails.core.settings import settings
from tests.api.data import testData


class TestGetUserList:
    def test_invalid_params(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/?limit=invalidd")
        assert response.status_code == 422

    def test_success(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/")
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) == 6
        testData.user0_uuid = response_json[0]["uuid"]

    def test_skip(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/?skip=4")
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) == 2

    def test_limit(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/?limit=2")
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) == 2


class TestGetUserByUUID:
    def test_invalid_user(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/gibberish_user_wont_exist")
        assert response.status_code == 404

    def test_success(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/user/{testData.user0_uuid}")
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["username"] == testData.USER0_USERNAME


class TestGetFollowersByUUID:
    def test_invalid_user(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/user/gibberish_user_wont_exist/followers"
        )
        assert response.status_code == 404

    def test_success(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/user/{testData.user0_uuid}/followers"
        )
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
        response = client.get(
            f"{settings.API_PREFIX}/user/{testData.user0_uuid}/following"
        )
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
        response = client.get(f"{settings.API_PREFIX}/user/{testData.user0_uuid}/pets")
        response_json = response.json()
        assert response.status_code == 200
        assert len(response_json) == 1


class TestGetLocationsByUUID:
    def test_invalid_user(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/user/gibberish_user_wont_exist/locations"
        )
        assert response.status_code == 404

    def test_success(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/user/{testData.user0_uuid}/locations"
        )
        response_json = response.json()
        assert response.status_code == 200
        assert response_json == []


class TestGetFavoritesByUUID:
    def test_invalid_user(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/user/gibberish_user_wont_exist/favorites"
        )
        assert response.status_code == 404

    def test_success(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/user/{testData.user0_uuid}/favorites"
        )
        response_json = response.json()
        assert response.status_code == 200
        assert response_json == []


class TestGetReviewsByUUID:
    def test_invalid_user(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/user/gibberish_user_wont_exist/reviews"
        )
        assert response.status_code == 404

    def test_success(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_PREFIX}/user/{testData.user0_uuid}/reviews"
        )
        response_json = response.json()
        assert response.status_code == 200
        assert response_json == []
