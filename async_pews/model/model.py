from dataclasses import InitVar, dataclass
from datetime import datetime, timedelta
from math import ceil, floor, pow, sqrt
from time import time
from typing import Mapping, TYPE_CHECKING


if TYPE_CHECKING:
    from async_pews.client.client import HTTPClient


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
    """
    지진 관련 정보들의 부모 클래스

    Attributes
    ----------
    lat: float
        진앙의 위도
    lon: float
        진앙의 경도
    depth: float
        진원의 깊이
    is_sea: bool
        해역 여부
    magnitude: float
        지진의 규모
    time: datetime
        지진 발생 시각
    max_intensity: int
        최대 진도
    max_intensity_area: list[str]
        최대 진도 지역
    earthquake_id: str | None
        지진 ID
    earthquake_str: str
        지진 위치 (ex. 제주 서귀포시 서남서쪽 32km 해역)
    """

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
    """
    지진속보의 정보를 담는 데이터클래스입니다.

    Attributes
    ----------
    lat: float
        진앙의 추정위도
    lon: float
        예상진앙의 추정경도
    depth: float
        진원의 추정깊이
    is_sea: bool
        해역 여부
    magnitude: float
        지진의 추정규모
    time: datetime
        지진 발생 추정시각
    max_intensity: int
        추정 최대 진도
    max_intensity_area: list[str]
        추정 최대 진도 지역
    earthquake_id: str | None
        지진 ID
    earthquake_str: str
        추정 지진 위치 (ex. 제주 서귀포시 서남서쪽 32km 해역)
    """

    _client: InitVar["HTTPClient"]

    def estimated_arrival_time(self, dest_lat: float, dest_lon: float) -> datetime:
        """
        입력한 위도와 경도 지점의 지진파 도달예측시각을 반환합니다.

        Parameters
        ----------
        dest_lat : float
            도달 예측을 원하는 위도
        dest_lon : float
            도달 예측을 원하는 경도

        Returns
        -------
        datetime
            지진파의 도달 예측 시각
        """
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

    def estimated_mmi(self, lat: float, lon: float) -> int:
        """
        입력한 위도와 경도 지점의 추정진도를 반환합니다.

        Parameters
        ----------
        lat : float
            위도
        lon : float
            경도

        Returns
        -------
        int
            추정 진도입니다.
            진도를 알 수 없는 지점일 경우 -1이 반환됩니다.

        Raises
        ------
        Exception
            Grid 정보의 수신에 실패하여 진도를 알 수 없는 경우 발생하는 에러입니다.
        """

        mag = -1

        if self.__client._grid_arr == []:
            raise Exception("Grid data is not loaded yet.")

        cnt = 0
        for i in range(3885, 3300, -5):
            for j in range(12450, 13205, 5):
                if abs(lat - i / 100) < 0.025 and abs(lon - j / 100) < 0.025:
                    mag = self.__client._grid_arr[cnt]

                    if mag > 11:
                        mag = 1

                    return mag

                cnt += 1

        return mag

    def __post_init__(self, client: "HTTPClient") -> None:
        self.__client = client
        self.__tide = client._tide


@dataclass
class EarthquakeInfo(EarthquakeEvent):
    """
    지진 정보를 담는 데이터클래스입니다.

    Attributes
    ----------
    lat: float
        진앙의 위도
    lon: float
        진앙의 경도
    depth: float
        진원의 깊이
    is_sea: bool
        해역 여부
    magnitude: float
        지진의 규모
    time: datetime
        지진 발생 시각
    max_intensity: int
        최대 진도
    max_intensity_area: list[str]
        최대 진도 지역
    earthquake_id: str | None
        지진 ID
    earthquake_str: str
        지진 위치 (ex. 제주 서귀포시 서남서쪽 32km 해역)
    """

    _client: InitVar["HTTPClient"]

    def get_mmi(self, lat: float, lon: float) -> int:
        """
        입력한 위도와 경도 지점의 분석된 진도를 반환합니다.

        Parameters
        ----------
        lat : float
            위도
        lon : float
            경도

        Returns
        -------
        int
            해당 지역의 진도입니다.
            진도를 알 수 없는 경우 -1이 반환됩니다.

        Raises
        ------
        Exception
            Grid 정보의 수신에 실패하여 진도를 알 수 없는 경우 발생하는 에러입니다.
        """
        mag = -1

        if self.__client._grid_arr == []:
            raise Exception("Grid data is not loaded yet.")

        cnt = 0
        for i in range(3885, 3300, -5):
            for j in range(12450, 13205, 5):
                if abs(lat - i / 100) < 0.025 and abs(lon - j / 100) < 0.025:
                    mag = self.__client._grid_arr[cnt]

                    if mag > 11:
                        mag = 1

                    return mag

                cnt += 1

        return mag

    def __post_init__(self, client: "HTTPClient") -> None:
        self.__client = client
