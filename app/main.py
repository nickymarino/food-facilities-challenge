import csv
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI

from app.location import Location
from app.mobile_facility import MobileFacility


FACILITIES: list[MobileFacility] = []


@asynccontextmanager
async def load_facilities(app: FastAPI):
    with open("app/Mobile_Food_Facility_Permit.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",", quotechar='"')

        # Read in all facilities
        for row_dict in reader:
            new_facility = MobileFacility.from_csv_row(row=row_dict)
            FACILITIES.append(new_facility)

    yield


app = FastAPI(lifespan=load_facilities)


@app.get("/")
def get_all_applicants() -> list[MobileFacility]:
    # Sanity check endpoint: return all facilities on GET /
    return FACILITIES


@app.get("/search/applicant")
def search_by_applicant(
    Applicant: str, Status: Optional[str] = None
) -> list[MobileFacility]:
    # Note: The challenge description doesn't specify whether the search
    # should be exact or partial match, or whether it should be case
    # sensitive.
    #
    # Because the street name search explicitly asks for partial searching,
    # I assume that the applicant name search should be an exact match.
    results = [facility for facility in FACILITIES if facility.Applicant == Applicant]

    # Further filter by status if provided
    if Status:
        results = [facility for facility in results if facility.Status == Status]

    return results


@app.get("/search/street")
def search_by_street(street: str) -> list[MobileFacility]:
    # Note: Based on the example "SAN" -> "SANSOME ST", I assumed this
    # search is case sensitive (in addition to a partial search).
    #
    # I also assume here that streets named "ST" should match the `street`
    # parameter. For example, "ST" should match "SANSOME ST". See README
    # for more details.
    results = [facility for facility in FACILITIES if street in facility.Address]
    return results


@app.get("/search/nearby")
def search_by_location(
    latitude: float, longitude: float, approved_only: bool = True
) -> list[MobileFacility]:
    location = Location(Latitude=latitude, Longitude=longitude)

    if approved_only:
        locations_to_search = [fac for fac in FACILITIES if fac.Status == "APPROVED"]
    else:
        locations_to_search = FACILITIES

    return location.find_closest_neighbors(
        other_locations=locations_to_search, num_neighbors=5
    )
