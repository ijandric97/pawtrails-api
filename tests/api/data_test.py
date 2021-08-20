from typing import Any, Dict


class TestData:
    TEST_EMAIL = "pytest@example.com"
    TEST_USERNAME = "pytest"
    TEST_PASSWORD = "password"

    bearer_token = ""
    my_uuid = ""

    USER0_USERNAME = "user0"
    user0_uuid = ""

    def bearer_header(self) -> Dict[str, Any]:
        return {"Authorization": f"Bearer {self.bearer_token}"}


testData = TestData()
