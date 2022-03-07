from dataclasses import dataclass
from datetime import datetime, timedelta
from math import floor, sqrt


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
    mag: int
    dep: float
    time: int
    max_intensity: int
    max_area: list
    sea: bool
    eqk_str: str

    def est_time(self, dest_lat: float, dest_lon: float) -> datetime:
        sec = floor(
            sqrt(((self.lat - dest_lat) * 111**2 + (self.lon - dest_lon) * 88**2))
            / 3
        )
