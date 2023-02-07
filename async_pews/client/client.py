import asyncio
from datetime import datetime, timedelta
from time import time
from typing import TYPE_CHECKING, Any
from urllib.parse import quote, unquote
from aiohttp import ClientSession

from ..exceptions.exceptions import HTTPStatusError
from ..model.model import EarthquakeEvent, Response, Station
from .CONSTANT import (
    BIN_PATH,
    DELAY,
    MAX_EQK_INFO_LEN,
    MAX_EQK_STR_LEN,
    TIDE,
    TZ_MSEC,
    SYNC_PERIOD,
    RA,
)
from .utils import Utils


class SessionManager:
    def __init__(self) -> None:
        self.__session: ClientSession | None = None

    async def __aenter__(self) -> ClientSession:
        self.__session = ClientSession()
        return self.__session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        assert self.__session
        await self.__session.close()

    @property
    def session(self) -> ClientSession | None:
        return self.__session


class HTTPClient:
    def __init__(self, sim: bool = False) -> None:

        # Name Mangling
        self.__session = SessionManager()
        self.__tide = TIDE
        self.__delay = DELAY
        self.__HEADER_LEN = 1 if sim else 4
        self.__bsync = True

        self._phase = 1
        self._eqk_event: EarthquakeEvent | None = None
        self._station_list: list[Station] = []

    # def __del__(self) -> None:
    #     asyncio.run(self.__session.close())

    @property
    def __time(self) -> int:
        return int(time() * 1000)

    @property
    def __pTime(self) -> str:
        return datetime.fromtimestamp(
            (self.__time - self.__tide - TZ_MSEC) // 1000
        ).strftime("%Y%m%d%H%M%S")

    async def _get(self, url: str) -> Response:
        async with self.__session as session:
            async with session.get(url) as resp:
                resp = Response(
                    resp.status,
                    await resp.read(),
                    resp.headers,
                )
        return resp

    async def _get_sta(
        self, url: str | None = None, data_str: str | None = None
    ) -> None:
        url = url or BIN_PATH + f"{self.__pTime}.s"
        print(url)
        resp = await self._get(url)

        if resp.status != 200:
            raise HTTPStatusError(
                resp.status,
                "Invaild HTTP status code received in __get_sta",
            )

        data = resp.data

        if not data:
            return

        byte_array = list(data)
        binary_str = ""

        for i in byte_array:
            binary_str += Utils.lpad(str(bin(i)[2:]), 8)

        await self.__sta_bin_handler(binary_str)

        if data_str:
            await self.__callback(data_str)

    async def _sync_interval(self) -> None:
        while True:
            await asyncio.sleep(SYNC_PERIOD)
            self._bSync = True

    async def __sta_bin_handler(self, data: str) -> None:
        sta_list = []
        sta_lat = []
        sta_lon = []

        for i in range(0, len(data), 20):

            sta_lat.append(30 + int(data[i : i + 10], 2) / 100)
            sta_lon.append(120 + int(data[i + 10 : i + 20], 2) / 100)

        for i in range(len(sta_lat)):
            sta_list.append(Station(sta_lat[i], sta_lon[i], i, -1))

        if len(sta_list) > 99:
            self._station_list = sta_list

    async def __callback(self, data: str) -> None:
        mmi = await self.__mmi_bin_handler(data)

        for i in range(len(self._station_list)):
            self._station_list[i].mmi = mmi[i]

    async def __mmi_bin_handler(self, data: str) -> list[int]:
        mmi_data = []

        if len(data) > 0:
            for i in range(0, len(data), 4):
                mmi_data.append(int(data[i : i + 4], 2))

        return mmi_data

    async def _get_MMI(self, url: str | None = None) -> None:
        url = url or BIN_PATH + f"{self.__pTime}.b"
        print(url, self.__tide)

        send_time = self.__time
        resp = await self._get(url)
        recv_time = self.__time

        if resp.status != 200:
            raise HTTPStatusError(
                resp.status,
                "Invaild HTTP status code received in __get_MMI",
            )
        headers = resp.headers

        if self.__bsync:
            st = headers["ST"].replace(".", "")

            # Time-Sync
            if self.__tide == self.__delay or recv_time - send_time < 100:
                self.__tide = self.__time - int(st) + self.__delay

            self.__bsync = False

        # Data Handle
        data = resp.data
        byte_array = list(data)

        header = ""
        binary_str = ""
        for i in range(self.__HEADER_LEN):
            header += Utils.lpad(bin(data[i])[2:], 8)

        for i in range(self.__HEADER_LEN, len(data)):
            binary_str += Utils.lpad(bin(data[i])[2:], 8)

        staF = header[0] == "1"

        if header[1] == header[2] == "0":
            if self._phase == 2 or self._phase == 3:
                self._phase = 1
        elif header[1] == "1" and header[2] == "0":
            self._phase = 2

        elif header[1] == "1" and header[2] == "1":
            self._phase = 3

        elif header[1] == "0" and header[2] == "1":
            self._phase = 4

        info_str_arr = []

        for i in range(len(byte_array) - MAX_EQK_STR_LEN, len(byte_array)):
            info_str_arr.append(byte_array[i])

        if staF or len(self._station_list) < 99:
            print("99 <")
            await self._get_sta(url.replace(".b", ".s"), binary_str)
        else:
            await self.__callback(binary_str)

        eqk_data = binary_str[0 - (MAX_EQK_STR_LEN * 8 + MAX_EQK_INFO_LEN) :]

        if self._phase == 2 or self._phase == 3:
            await self.__fn_eqk_handler(eqk_data, info_str_arr)
        elif self._phase == 4:
            eqk_id = self.__parse_eqk_id(eqk_data)

            if self._eqk_event:
                self._eqk_event.eqk_id = eqk_id

    async def __fn_eqk_handler(self, eqk_data: str, info_str_arr: list[str]) -> None:
        origin_lat = 30 + int(eqk_data[0:10], 2) / 100
        origin_lon = 120 + int(eqk_data[10:20], 2) / 100
        eqk_mag = int(eqk_data[20:27], 2) / 10
        eqk_depth = int(eqk_data[27:32], 2) / 10
        eqk_time = int(eqk_data[37:69], 2) * 1000
        eqk_id = "20" + str(int(eqk_data[69:95], 2)) if eqk_data else None
        eqk_max = int(eqk_data[95:99], 2)
        eqk_max_area = []
        _eqk_max_area_str = eqk_data[99:116]

        if _eqk_max_area_str != "11111111111111111":
            for i in range(17):
                if _eqk_max_area_str[i] == "1":
                    eqk_max_area.append(RA.ko[i])

        eqk_str = unquote(
            quote(
                "".join([chr(int(x)) for x in info_str_arr]),
                encoding="raw_unicode_escape",
            )
        ).strip()
        eqk_sea = eqk_str.find("해역") != -1

        self._eqk_event = EarthquakeEvent(
            origin_lat,
            origin_lon,
            eqk_depth,
            eqk_sea,
            eqk_mag,
            datetime.fromtimestamp(eqk_time // 1000) + timedelta(hours=9),
            eqk_max,
            eqk_max_area,
            eqk_id,
            eqk_str,
        )

    def __parse_eqk_id(self, eqk_data: str) -> str | None:
        return "20" + str(int(eqk_data[69:95], 2)) if eqk_data else None


if __name__ == "__main__":
    HTTPClient()
