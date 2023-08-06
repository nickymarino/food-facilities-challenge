from app.mobile_facility import MobileFacility


def new_mock_facility(
    locationid: int, latitude: float, longitude: float, status: str = "APPROVED"
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
        Status=status,
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
