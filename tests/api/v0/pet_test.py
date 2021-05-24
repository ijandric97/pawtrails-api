from fastapi.testclient import TestClient

from pawtrails.core.settings import settings


class TestPetList:
    def test_success(self, client: TestClient) -> None:
        response = client.get(f"{settings.API_PREFIX}/pet")
        assert response.status_code == 200
        # assert response_json == "" TODO
