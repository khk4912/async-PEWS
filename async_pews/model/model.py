from dataclasses import dataclass


@dataclass
class Station:
    lat: float
    lon: float
    idx: int
