from dataclasses import dataclass
import discord


@dataclass
class Station:
    lat: float
    lon: float
    idx: int
    mmi: int | None = None
    name: str | None = None
