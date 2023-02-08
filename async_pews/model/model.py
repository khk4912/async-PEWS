from dataclasses import InitVar, dataclass
from datetime import datetime, timedelta
from math import ceil, floor, pow, sqrt
from time import time
from typing import Mapping


@dataclass
class Station:
    lat: float
    lon: float
    idx: int
    mmi: int


@dataclass
class Response:
    status: int
    data: bytes
    headers: Mapping[str, str]


@dataclass
class EarthquakeEvent:
    lat: float
    lon: float
    depth: float
    is_sea: bool
    magnitude: float
    time: datetime
    max_intensity: int
    max_intensity_area: list[str]
    earthquake_id: str | None
    earthquake_str: str


@dataclass
class EarlyWarningInfo(EarthquakeEvent):
    _tide: InitVar[int]

    def estimated_arrival_time(self, dest_lat: float, dest_lon: float) -> datetime:
        sec = floor(
            sqrt(
                (pow((self.lat - dest_lat) * 111, 2))
                + (pow((self.lon - dest_lon) * 88, 2))
            )
            / 3
        ) - (
            ceil(int(time() * 1000) - self.__tide - int(self.time.timestamp() * 1000))
            / 1000
        )

        return datetime.now() + timedelta(seconds=sec)

    def __post_init__(self, tide: int) -> None:
        self.__tide = tide


@dataclass
class EarthquakeInfo(EarthquakeEvent):
    ...
