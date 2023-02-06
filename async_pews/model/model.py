from dataclasses import dataclass
from typing import Mapping, Any


@dataclass
class Station:
    lat: float
    lon: float
    idx: int


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
    time: int
    max_intensity: int
    max_intensity_area: list[str]
    eqk_id: str | None
    eqk_str: str
