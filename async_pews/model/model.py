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
    headers: Mapping[str, Any]
