from time import time
from datetime import datetime, timedelta
from math import floor, ceil, sqrt, pow
from dataclasses import dataclass, InitVar
from typing import Mapping

from ..client.CONSTANT import TZ_MSEC


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
