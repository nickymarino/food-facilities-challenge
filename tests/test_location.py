import pytest

from app.location import Location


def test_distance_miles_from_returns_distance_in_miles():
    # Examples calculated using the Median Outpost Latitude/Longitude Distance Calculator
    #
    # https://www.meridianoutpost.com/resources/etools/calculators/calculator-latitude-longitude-distance.php?

    location1 = Location(Latitude=37.0, Longitude=-122.0)
    location2 = Location(Latitude=37.0, Longitude=-122.1)
    assert location1.distance_miles_from(location2) == pytest.approx(5.52, rel=0.01)

    location3 = Location(Latitude=37.1, Longitude=-123.0)
    location4 = Location(Latitude=37.2, Longitude=-122.1)
    assert location3.distance_miles_from(location4) == pytest.approx(50.04, rel=0.01)


def test_find_closest_neighbors_fail_if_asked_for_too_many():
    location1 = Location(Latitude=37.0, Longitude=-122.0)
    location2 = Location(Latitude=37.0, Longitude=-122.1)
    other_locations = [location2]

    with pytest.raises(ValueError):
        location1.find_closest_neighbors(other_locations, num_neighbors=3)


def test_find_closest_single_neighbor_with_mock_locations():
    location1 = Location(Latitude=37.0, Longitude=-122.0)
    location2 = Location(Latitude=37.0, Longitude=-122.1)
    location3 = Location(Latitude=30, Longitude=-120)
    other_locations = [location2, location3]

    actual_closest = location1.find_closest_neighbors(other_locations, num_neighbors=1)
    expected_closest = [location2]
    assert actual_closest == expected_closest


def test_find_closest_multiple_neighbors_with_mock_locations():
    location1 = Location(Latitude=37.0, Longitude=-122.0)
    location2 = Location(Latitude=37.0, Longitude=-122.1)
    location3 = Location(Latitude=37.1, Longitude=-121.1)
    location4 = Location(Latitude=30, Longitude=-120)
    other_locations = [location2, location3, location4]

    actual_closest = location1.find_closest_neighbors(other_locations, num_neighbors=2)
    expected_closest = [location2, location3]
    assert actual_closest == expected_closest
