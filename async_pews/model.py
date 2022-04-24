from dataclasses import InitVar, dataclass
from datetime import datetime, timedelta
from math import ceil, floor, sqrt
from time import time


from .constant import TZ_MSEC, Region


# def float_range(start: float, stop: float, step: float) -> Iterator[float]:
#     while start < stop:
#         yield start
#         start += step


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
    _grid_arr: InitVar[list[int]]
    _tide: InitVar[int]

    def est_time(self, dest_lat: float, dest_lon: float) -> datetime:
        sec = floor(
            sqrt(
                (((self.lat - dest_lat) * 111) ** 2 + ((self.lon - dest_lon) * 88) ** 2)
            )
            / 3
        ) - (
            ceil(int(time() * 1000) - self.__tide - int(self.time.timestamp() * 1000))
            / 1000
        )
        # print(sec)
        return datetime.now() + timedelta(seconds=sec)

    def est_mag(self, dest_lat: float, dest_lon: float) -> int:
        cnt = 0
        if len(self.__grid_arr) > 0:
            for i in map(lambda x: x / 100, range(3885, 3299, -5)):
                for j in map(lambda x: x / 100, range(12450, 13205, 5)):
                    if abs(dest_lat - i) < 0.025 and abs(dest_lon - j) < 0.025:
                        mag = self.__grid_arr[cnt]

                        if mag > 11:
                            mag = 1

                        return mag

                    cnt += 1

            return 1
        else:
            return 1

    def __post_init__(
        self,
        _grid_arr: list[int],
        _tide: int,
    ):
        self.__grid_arr = _grid_arr
        self.__tide = _tide


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
