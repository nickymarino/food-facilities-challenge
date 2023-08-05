import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """
    Use the TestClient as a scope to activate the lifespan context manager,
    which loads the facilities from the CSV file.
    """
    with TestClient(app) as client:
        yield client


def test_get_root_returns_all_facilities(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200

    response_json = response.json()
    assert type(response_json) == list
    assert len(response_json) == 488

    # Sanity check: verify the first location ID matches
    first_facility = response_json[0]
    assert first_facility["locationid"] == 1571753


class TestSearchByApplicant:
    def test_exact_match_with_one_applicant_returns_one_facility(
        self, client: TestClient
    ):
        response = client.get(
            "/search/applicant", params={"Applicant": "The Geez Freeze"}
        )
        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json) == list
        assert len(response_json) == 1
        assert response_json[0]["locationid"] == 1571753

    def test_partial_match_with_one_applicant_returns_no_facilities(
        self, client: TestClient
    ):
        response = client.get("/search/applicant", params={"Applicant": "Geez"})
        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json) == list
        assert len(response_json) == 0

    def test_match_with_multiple_facilities_returns_multiple_facilities(
        self, client: TestClient
    ):
        response = client.get(
            "/search/applicant", params={"Applicant": "Kettle Corn Star"}
        )
        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json) == list

        location_ids = set([row["locationid"] for row in response_json])
        expected_ids = set([1341056, 1336921])
        assert location_ids == expected_ids

    def test_status_with_no_matches_returns_no_facilities(self, client: TestClient):
        response = client.get(
            "/search/applicant",
            params={"Applicant": "Kettle Corn Star", "Status": "APPROVED"},
        )
        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json) == list
        assert len(response_json) == 0

    def test_status_with_matches_returns_filtered_facilities(self, client: TestClient):
        response = client.get(
            "/search/applicant",
            params={"Applicant": "San Pancho's Tacos", "Status": "APPROVED"},
        )
        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json) == list

        location_ids = set([row["locationid"] for row in response_json])
        expected_ids = set([1598473, 1598475, 1598474])
        assert location_ids == expected_ids
