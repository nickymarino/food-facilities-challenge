from __future__ import annotations

from geopy.distance import distance
from pydantic import BaseModel


class Location(BaseModel):
    # Note: These values are capitalized to match the format for MobileFacility.
    # See README for more details.
    Latitude: float
    Longitude: float

    @property
    def lat_long(self) -> tuple[float, float]:
        """Return a tuple of the latitude and longitude"""
        return (self.Latitude, self.Longitude)

    def distance_miles_from(self, other: Location) -> float:
        """Return the distance in miles between this facility and another"""
        return distance(self.lat_long, other.lat_long).miles

    def find_closest_neighbors(
        self, other_locations: list[Location], num_neighbors: int
    ) -> list[Location]:
        """
        Return a list of the `num_neighbors` closest locations with the
        specified status.
        """
        # Fail if there are more neighbors requested than we can provide
        if num_neighbors > len(other_locations):
            raise ValueError(
                f"Cannot find {num_neighbors} neighbors when there are only {len(other_locations)} facilities"
            )

        # search = [(l.lat_long, self.distance_miles_from(l)) for l in other_locations]
        # search.sort(key=lambda x: x[1])
        # from pprint import pprint

        # pprint(search[:5])
        # Sort facilities by distance from this facility
        examined_locations = sorted(
            other_locations, key=lambda location: self.distance_miles_from(location)
        )

        # Return the `num_neighbors` closest facilities
        return examined_locations[:num_neighbors]
