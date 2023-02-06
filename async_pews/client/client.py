import asyncio
from datetime import datetime
from multiprocessing.connection import Client
from time import time
from typing import TYPE_CHECKING, Any

from aiohttp import ClientResponse, ClientSession

from ..exceptions.exceptions import HTTPStatusError
from ..model.model import Response, Station
from .CONSTANT import BIN_PATH, DELAY, MAX_EQK_INFO_LEN, MAX_EQK_STR_LEN, TIDE, TZ_MSEC
from .utils import Utils


class SessionManager:
    def __init__(self) -> None:
        self.__session: ClientSession | None = None

    async def __aenter__(self) -> ClientSession:
        self.__session = ClientSession(timeout=1000)
        return self.__session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    async def close_session(self) -> None:
        if self.__session:
            await self.__session.close()

    @property
    def session(self) -> ClientSession | None:
        return self.__session


class HTTPClient:
    def __init__(self) -> None:

        # Name Mangling
        self.__session = SessionManager()
        self.__tide = TIDE
        self.__delay = DELAY
        self.__clock = self.__time
        self.__HEADER_LEN = 4

        self._phase = 1
        self._station_list: list[Station] = []

    def __del__(self) -> None:
        asyncio.run(self.__session.close_session())

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
            async with session.get(url, timeout=1) as resp:
                return Response(
                    resp.status,
                    await resp.read(),
                    resp.headers,
                )

    async def __get_sta(
        self, url: str | None = None, data_str: str | None = None
    ) -> None:
        url = url or BIN_PATH + f"{self.__pTime}.s"

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
            binary_str += Utils.lpad(bin(i)[2:], 8)

        await self.__sta_bin_handler(binary_str)

        if data_str:
            await self.__callback(data_str)

    async def __sta_bin_handler(self, data: str) -> None:
        sta_list = []
        sta_lat = []
        sta_lon = []

        for i in range(0, len(data), 20):
            sta_lat.append(30 + int(data[i : i + 10], 2) / 100)
            sta_lon.append(120 + int(data[i + 10 : i + 20], 2) / 100)

        for i in range(len(sta_lat)):
            sta_list.append(Station(sta_lat[i], sta_lon[i], i))

        if len(sta_list) > 99:
            self.station_list = sta_list

    async def __callback(self, data: str) -> None:
        pass

    async def __get_MMI(self, url: str | None = None) -> None:
        url = url or BIN_PATH + f"{self.__pTime}.b"

        send_time = self.__time
        resp = await self._get(url)
        recv_time = self.__time

        if resp.status != 200:
            raise HTTPStatusError(
                resp.status,
                "Invaild HTTP status code received in __get_MMI",
            )
        headers = resp.headers

        st = headers["ST"].replace(".", "")
        last_modified = headers["Last-Modified"]

        # Time-Sync
        if self.__tide == self.__delay or recv_time - send_time < 100:
            self.__tide = self.__time - int(st) + self.__delay

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

        for i in range(len(byte_array) - MAX_EQK_INFO_LEN, len(byte_array)):
            info_str_arr.append(binary_str[i])

        if staF or len(self._station_list) < 99:
            await self.__get_sta(url, binary_str)
        else:
            await self.__callback(binary_str)

        eqk_data = binary_str[0 - (MAX_EQK_STR_LEN * 8 + MAX_EQK_INFO_LEN) :]

        if self._phase == 2 or self._phase == 3:
            await self.__fn_eqk_handler(eqk_data, info_str_arr)
        elif self._phase == 4:
            await self._fn_parse_eqk_id(eqk_data)

    async def __fn_eqk_handler(self, eqk_data: str, info_str_arr: list[str]) -> None:
        pass

    async def _fn_parse_eqk_id(self, eqk_data: str) -> None:
        pass


if __name__ == "__main__":
    HTTPClient()
