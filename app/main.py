import csv
from contextlib import asynccontextmanager

from fastapi import FastAPI

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
def search_by_applicant(applicant: str) -> list[MobileFacility]:
    # Sanity check endpoint: return all facilities on GET /
    return FACILITIES


@app.get("/search/applicant")
def search_by_applicant(applicant: str) -> list[MobileFacility]:
    # Note: The challenge description doesn't specify whether the search
    # should be exact or partial match, or whether it should be case
    # sensitive.
    #
    # Because the street name search explicitly asks for partial searching,
    # I assume that the applicant name search should be an exact match.
    results = [fac for fac in FACILITIES if fac.Applicant == applicant]
    print(FACILITIES[0].Applicant)
    return results
