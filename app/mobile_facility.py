from __future__ import annotations

from typing import Optional

from geopy.distance import distance
from pydantic import BaseModel, validator


class MobileFacility(BaseModel):
    locationid: int
    Applicant: str
    FacilityType: str
    cnn: int
    LocationDescription: str
    Address: str
    blocklot: str
    block: str
    lot: str
    permit: str
    Status: str
    FoodItems: str
    X: str
    Y: str
    Latitude: float
    Longitude: float
    Schedule: str
    dayshours: str
    NOISent: str
    Approved: str
    Received: str
    PriorPermit: int
    ExpirationDate: str
    Location: str
    FirePreventionDistricts: Optional[int]
    PoliceDistricts: Optional[int]
    SupervisorDistricts: Optional[int]
    ZipCodes: Optional[int]
    NeighborhoodsOld: Optional[int]

    @validator(
        "FirePreventionDistricts",
        "PoliceDistricts",
        "SupervisorDistricts",
        "ZipCodes",
        "NeighborhoodsOld",
        pre=True,
    )
    def empty_str_to_none(cls, value):
        """
        Convert all fields that expect a number to None if the value is an
        empty string
        """
        if value == "":
            return None
        return value

    @property
    def lat_long(self) -> tuple[float, float]:
        """Return a tuple of the latitude and longitude"""
        return (self.Latitude, self.Longitude)

    def distance_miles_from(self, other: MobileFacility) -> float:
        """Return the distance in miles between this facility and another"""
        return distance(self.lat_long, other.lat_long).miles

    @classmethod
    def from_csv_row(cls, row: dict) -> MobileFacility:
        """Create an instance of this class from a CSV `DictReader` row"""
        # Rename CSV keys with spaces into CamelCase
        keys_to_rename = [
            ("Fire Prevention Districts", "FirePreventionDistricts"),
            ("Police Districts", "PoliceDistricts"),
            ("Supervisor Districts", "SupervisorDistricts"),
            ("Zip Codes", "ZipCodes"),
            ("Neighborhoods (old)", "NeighborhoodsOld"),
        ]
        for old_key, new_key in keys_to_rename:
            row[new_key] = row.pop(old_key)

        return cls(**row)
