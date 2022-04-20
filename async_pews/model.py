from dataclasses import dataclass
from datetime import datetime
from math import floor, sqrt

from .constant import Region


@dataclass
class Station:
    lat: float
    lon: float
    idx: int
    mmi: int | None = None
    name: str | None = None


@dataclass
class EEWInfo:
    lat: float
    lon: float
    mag: float
    dep: float
    time: datetime
    max_intensity: int
    max_area: list[Region]
    sea: bool
    eqk_str: str

    def est_time(self, dest_lat: float, dest_lon: float):
        sec = floor(
            sqrt(((self.lat - dest_lat) * 111**2 + (self.lon - dest_lon) * 88**2))
            / 3
        )


@dataclass
class EqkInfo:
    lat: float
    lon: float
    mag: float
    dep: float
    time: datetime
    max_intensity: int
    max_area: list[Region]
    sea: bool
    eqk_str: str
