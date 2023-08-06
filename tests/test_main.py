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

        location_ids = [row["locationid"] for row in response_json]
        expected_ids = [1341056, 1336921]
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

        location_ids = [row["locationid"] for row in response_json]
        expected_ids = [1598473, 1598475, 1598474]
        assert location_ids == expected_ids


class TestSearchByStreet:
    def test_partial_street_search_returns_proper_facilities(self, client: TestClient):
        response = client.get(
            "/search/street",
            params={"street": "SAN"},
        )
        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json) == list

        assert len(response_json) == 7

        location_ids_and_addresses = [
            (row["locationid"], row["Address"]) for row in response_json
        ]
        expected_ids_and_addresses = [
            (1591820, "217 SANSOME ST"),
            (934719, "1 SANSOME ST"),
            (1591839, "1 SANSOME ST"),
            (1585966, "727 SANSOME ST"),
            (934518, "115 SANSOME ST"),
            (934555, "231 SANSOME ST"),
            (1337923, "155 SANSOME ST"),
        ]
        assert location_ids_and_addresses == expected_ids_and_addresses

    def test_partial_lowercase_street_search_returns_no_facilities(
        self, client: TestClient
    ):
        response = client.get(
            "/search/street",
            params={"street": "san"},
        )
        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json) == list
        assert len(response_json) == 0

    def test_partial_nonexisting_street_search_returns_no_facilities(
        self, client: TestClient
    ):
        response = client.get(
            "/search/street",
            params={"street": "definitely-not-a-street-name"},
        )
        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json) == list
        assert len(response_json) == 0


class TestSearchNearby:
    """
    The following tests use the following coordinates:

        Location ID: 1565954
        Applicant: Treats by the Bay LLC
        Latitude: 37.78924953407508
        Longitude: -122.40241859729358

        Manual analysis for the nearest neighbors (location ID, distance, status):
        [
            (1565954, 0.0, "APPROVED"),
            (1589653, 0.0, "APPROVED"),
            (1576374, 0.0, "APPROVED"),
            (934517, 0.01657348314658408, "EXPIRED"),
            # Note: the next two are tied
            (1585464, 0.033574074938215744, "APPROVED"),
            (934553, 0.033574074938215744, "EXPIRED"),
            (1585472, 0.03395497936972788, "APPROVED"),
            (1042438, 0.08178558325197138, "REQUESTED"),
            (1337926, 0.08178558325197138, "REQUESTED"),
        ]

        Location ID: 1590833
        Applicant: El Alambre
        Latitude: 37.76785244271805
        Longitude: -122.41610489253189

        Manual analysis for the nearest neighbors (location ID, distance, status):
        [
            (1590834, 0.0, 'APPROVED'),
            (1590833, 0.0, 'APPROVED'),
            (751253, 0.0, 'REQUESTED'),
            (1587562, 0.07280574469168964, 'APPROVED'),
            (1332941, 0.1577400719482267, 'EXPIRED'),
            (953198, 0.21574497480501592, 'EXPIRED'),
            (1336734, 0.21949440273058746, 'EXPIRED'),
            (1163790, 0.22689235547856157, 'REQUESTED'),
            (1568966, 0.2401130478795503, 'APPROVED'),
            (1034228, 0.24402899281168797, 'REQUESTED'),
            (1568965, 0.24476063229752, 'APPROVED'),
        ]
    """

    @pytest.mark.parametrize(
        "latitude, longitude, expected_location_ids",
        [
            (
                37.78924953407508,
                -122.40251859729358,  # Tweaked to -122.4025 to prevent a tie
                [1565954, 1589653, 1576374, 1585464, 1585472],
            ),
            (
                37.76785244271805,
                -122.41610489253189,
                [1590834, 1590833, 1587562, 1568966, 1568965],
            ),
        ],
    )
    def test_default_search_only_shows_approved_locations(
        self,
        client: TestClient,
        latitude: float,
        longitude: float,
        expected_location_ids: list[int],
    ):
        response = client.get(
            "/search/nearby", params={"latitude": latitude, "longitude": longitude}
        )
        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json) == list
        assert len(response_json) == 5

        location_ids = [row["locationid"] for row in response_json]
        assert location_ids == expected_location_ids

    @pytest.mark.parametrize(
        "latitude, longitude, expected_location_ids",
        [
            (
                37.78924953407508,
                -122.40251859729358,  # Tweaked to -122.4025 to prevent a tie
                [1565954, 1589653, 1576374, 934517, 1585464],
            ),
            (
                37.76785244271805,
                -122.41610489253189,
                [1590834, 1590833, 751253, 1587562, 1332941],
            ),
        ],
    )
    def test_search_all_statuses_shows_all_closest_locations(
        self,
        client: TestClient,
        latitude: float,
        longitude: float,
        expected_location_ids: list[int],
    ):
        response = client.get(
            "/search/nearby",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "approved_only": False,
            },
        )
        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json) == list
        assert len(response_json) == 5

        location_ids = [row["locationid"] for row in response_json]
        assert location_ids == expected_location_ids
