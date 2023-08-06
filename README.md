# Food Facilities Challenge - Writeup

## Overview

This project implements an HTTP REST API on top of a [dataset of Mobile Food Facilities in San Francisco](https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat/data). There are several endpoints that enable an end user to search by various facility features, such as applicant name and street address. See [CHALLENGE.md](CHALLENGE.md) for the full set of requirements and [**Endpoints and Documentation**](#endpoints-and-documentation) for a description of each endpoint.

## Solution

This solution is a [FastAPI](https://fastapi.tiangolo.com/) project. The data store is the provided CSV file, and the CSV file is read into the app as a [lifespan function](https://fastapi.tiangolo.com/advanced/events/#lifespan-function) on startup. The end user can call this solution's HTTP REST endpoints to query the data. (See [**How to Run**](#how-to-run) for details.)

### Technical Decisions

- Because the dataset is < 500 rows, and because this is a take-home challenge designed to complete in 3-4 hours, **I decided to read the CSV into memory as the datastore** instead of using a database such as [SQLite](https://www.sqlite.org/index.html) or [PostgreSQL](https://www.postgresql.org/). This would likely be the first thing I would change to "productionize" this project.
- Because there are bonus points for using an API documentation tool, **I decided to use FastAPI** instead of other tools such as Flask or Django because it can provide OpenAPI-compatible documentation (and an interactive doc!) out of the box.
- **I chose to implement this as a REST API** instead of a GraphQL API because I am more familiar with the REST pattern, especially when coupled with FastAPI.
- **I chose Docker as my deploy strategy** because the challenge gives us bonus points for providing specifically a `Dockerfile` :) Docker is also generally a good strategy for packaging this API because it can integrate with many deployment tools such as AWS ECS, Kubernetes, Docker Swarm, etc.

## Critique

### What would you have done differently if you had spent more time on this?

I had more time to spend on this project, I would have converted the datastore into a proper database such as [SQLite](https://www.sqlite.org/index.html) or [PostgreSQL](https://www.postgresql.org/). This would be the first thing I'd likely do to "productionize" this app, as a CSV won't scale to a large number of objects, and right now the project  just keeps all locations in memory.

I would have also liked to deploy this app to a cloud provider so that the team could see this live, such as using an AWS API Gateway.

After that, I would continue investing time into the trade offs and scaling features detailed in the next questions.

### What are the trade-offs you might have made?

The largest trade-off I made was to read the CSV into memory as the datastore instead of a database, in the interest of time and simplicity and because this is a take-home challenge.

The second largest trade-off is the algorithm to calculate the 5 nearest food trucks. I used [geopy's distance equation](https://geopy.readthedocs.io/en/stable/#module-geopy.distance) and verified its results using [Median Outpost's Distance Calculator](https://www.meridianoutpost.com/resources/etools/calculators/calculator-latitude-longitude-distance.php?). My algorithm calculates the distance of each facility from the requested coordinates and then sorts them all by ascending distance. With < 500 rows, this approach is fine for now; however, the algorithm has a `O(n)` complexity and will not scale to thousands or more facilities.

### What are the things you left out?

I did not include nicer error handling outside of what pydantic and FastAPI provide out of the box (type checking on the CSV reading and API input/output schema validation, respectively). In a future version, this project could examine each row in the CSV and pretty-print validation errors for any invalid row(s) before the application starts.

The street search algorithm is naive and only checks whether the user's text input exists in the `Address` field. A better way to implement this is to parse each address for the street name itself and search from that. For example, searching for `ST` will return any locations that are on a road named street (`ST`), but the search should just return roads with `ST` in the name such as `01ST`.

I also did not invest time in reading in CSV properties that were not core to the requested use cases; for example, there are several datetime columns in the CSV that could be read into Python `datetime` instances in a future version of this project, such as `NOISent` and `ExpirationDate`.

In general, the columns from the CSV don't have one standard format, and a future version of this project could create a standard format for all fields. For example, the fields `locationid` and `Neighborhoods (Old)` could be returned as `location_id` and `neighborhoods_old`.

### What are the problems with your implementation and how would you solve them if we had to scale the application to a large number of users?

As stated above, the datastore **must** be migrated from in-memory to a database or document storage solution to properly scale.

For a large number of end users and facilities, the nearby location search algorithm must be modified to not have an `O(n)` complexity. There are several better solutions for this at scale, such as using [PostGIS](https://postgis.net/) as a geographic/spatial database or storing the facilities in an [R-tree](https://rd.springer.com/chapter/10.1007/11733836_68) for an optimal nearest-neighbor search.

The API should include better error validation. For example, the `Status` field is used in several places as a string input. A future version of this project should convert `Status` into an enum and require the user to select from the known valid statuses.

The tests in this solution currently mostly validate key fields are returned correctly, such as `locationid` and `Applicant`. To properly scale, the tests should be modified to verify that all fields are properly returned, such as `NOISent`, `Zip Codes`, etc.

From a security standpoint, an authentication strategy such as API keys or OAuth should be implemented along with rate limiting to prevent misuse and DOS attacks.

## How to Run

This project includes a `Makefile`. To see a list of all available commands, run `make help`:

```text
$ make help

help:      Show this help.
build:     Build a Docker image of this project
run:       Run the Docker image of this project
install:   Installs this package for local dev and testing
dev:       Run a local dev version of this project
test:      Run the test suite
```

To build a Docker image of the project and run it as a container, run `make build run`, and then go to `http://0.0.0.0:80/docs` to view the interactive API. (See the **Endpoints and Documentation** section below for more details.)

```text
$ make build run

docker build -t marino-nicky-food-facilities-challenge:latest .
...

docker run -p 80:80 marino-nicky-food-facilities-challenge:latest
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

To install the project locally and run unit tests, run `make install test`:

```text
$ make install test

pip3 install -r requirements.dev.txt
...

pytest
============================ test session starts =============================
platform darwin -- Python 3.9.4, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/.../food-facilities-challenge
plugins: anyio-3.7.1
collected 18 items

tests/test_location.py ....                                            [ 22%]
tests/test_main.py .............                                       [ 94%]
tests/test_mobile_facility.py .                                        [100%]

============================= 18 passed in 0.36s =============================
```

### Endpoints and Documentation

The interactive docs and OpenAPI specification for the API are available at these locations depending on which `make` command you used to run the project:

| Command | Interactive Docs | OpenAPI Spec |
| ------- | ---------------- | ------------ |
| `make build run` | `http://0.0.0.0:80/docs` | `http://0.0.0.0:80/openapi.json` |
| `make install dev` | `http://0.0.0.0:8000/docs` | `http://0.0.0.0:8000/openapi.json` |

Here is a brief overview of each endpoint:

| Endpoint | Description | Notes |
| ------- | ------------ | ----- |
| `GET /` | Return a list of all facilities |
| `GET /search/applicant` | Return all facilities with that applicant's name and optional status. | Case sensitive and exact match (not partial). |
| `GET /search/street` | Return all facilities with that street's name. | Case sensitive and partial match. |
| `GET /search/nearby` | Return the 5 facilities closest to a particular lat/long. | Default to `APPROVED` status only. Set `approved_only=False` to look at all facilities. |

## Meta

**Note:** This project was tested locally on macOS Ventura 13.5 and Python 3.9.4 on an M1 chip, and on the image specified in the `Dockerfile`. This project has _not_ been tested on an Intel Mac or Windows/Linux.

This project took ~4 hours to complete followed by ~30 minutes of adding README documentation.
