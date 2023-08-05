from pytest import approx

from app.mobile_facility import MobileFacility


def new_mock_facility(
    locationid: int, latitude: float, longitude: float
) -> MobileFacility:
    """
    Hydrate a `MobileFacility` instance with mock data
    """
    return MobileFacility(
        locationid=locationid,
        Applicant=f"applicant-{locationid}",
        FacilityType="Truck",
        cnn=887000,
        LocationDescription="Description of the location",
        Address="8 10TH ST",
        blocklot="3721120",
        block="3721",
        lot="120",
        permit="21MFF-00015",
        Status="APPROVED",
        FoodItems="Tacos, burritos",
        X="100",
        Y="100",
        Latitude=latitude,
        Longitude=longitude,
        Schedule="All day every day",
        dayshours="Mo:6AM-8PM",
        NOISent="",
        Approved="01/28/2022 12:00:00 AM",
        Received="20210315",
        PriorPermit=0,
        ExpirationDate="11/15/2022 12:00:00 AM",
        Location=f"({latitude}, {longitude})",
        FirePreventionDistricts=8,
        PoliceDistricts=4,
        SupervisorDistricts=5,
        ZipCodes=64,
        NeighborhoodsOld=14,
    )


def test_lat_long_returns_tuple():
    facility = new_mock_facility(1, 37.0, -122.0)
    assert facility.lat_long == (37.0, -122.0)


def test_distance_miles_from_returns_distance_in_miles():
    # Examples calculated using the Median Outpost Latitude/Longitude Distance Calculator
    #
    # https://www.meridianoutpost.com/resources/etools/calculators/calculator-latitude-longitude-distance.php?

    facility1 = new_mock_facility(1, 37.0, -122.0)
    facility2 = new_mock_facility(2, 37.0, -122.1)
    assert facility1.distance_miles_from(facility2) == approx(5.52, rel=0.01)

    facility3 = new_mock_facility(1, 37.1, -123.0)
    facility4 = new_mock_facility(2, 37.2, -122.1)
    assert facility3.distance_miles_from(facility4) == approx(50.04, rel=0.01)
