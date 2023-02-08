from datetime import datetime
from dataclasses import dataclass
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
