import asyncio
import json
import logging
from datetime import datetime, timedelta
from time import time
from typing import Type
from urllib.parse import quote, unquote


from ..exceptions.exceptions import HTTPStatusError
from ..model.model import EarthquakeEvent, Station
from .CONSTANT import (
    BIN_PATH,
    DELAY,
    MAX_EQK_INFO_LEN,
    MAX_EQK_STR_LEN,
    RA,
    SYNC_PERIOD,
    TIDE,
    TZ_MSEC,
)
from .session import SessionClient
from .utils import Utils


class HTTPClient:
    def __init__(self, sim: bool = False) -> None:
        # Name Mangling
        self.__client = SessionClient()
        self._tide = TIDE
        self.__delay = DELAY
        self.__HEADER_LEN = 1 if sim else 4
        self.__bsync = True
        self.__grid_renew = True
        self.__sim = sim

        self._phase = 1
        self._eqk_event: EarthquakeEvent | None = None
        self._grid_arr: list[int] = []
        self._station_list: list[Station] = []
        self.__logger = logging.getLogger("async_pews")

        self._ongoing_events: list[Type[EarthquakeEvent]] = []

    # def __del__(self) -> None:
    #     asyncio.run(self.__session.close())

    @property
    def __time(self) -> int:
        return int(time() * 1000)

    @property
    def __pTime(self) -> str:
        return datetime.fromtimestamp(
            (self.__time - self._tide - TZ_MSEC) // 1000
        ).strftime("%Y%m%d%H%M%S")

    async def __get_location(self, eqk_id: str, phase: int) -> dict[str, str] | None:
        if self.__sim:
            url = BIN_PATH + f"{eqk_id}/"
        else:
            url = BIN_PATH

        url += f"{eqk_id}.le" if phase == 2 else f"{eqk_id}.li"

        try:
            resp = await self.__client.get(url)
        except Exception as err:
            self.__logger.warn("Failed to get location data!")
            self.__logger.debug("Error: ", err)
            return

        data = resp.data
        return json.loads(data)

    async def _get_sta(
        self, url: str | None = None, data_str: str | None = None
    ) -> None:
        url = url or BIN_PATH + f"{self.__pTime}.s"

        try:
            resp = await self.__client.get(url)
        except Exception as err:
            self.__logger.warn("Failed to get station data!")
            self.__logger.debug("Error: ", err)
            return

        if resp.status != 200:
            raise HTTPStatusError(
                resp.status,
                "Invalid HTTP status code received in __get_sta",
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
        sta_list: list[Station] = []
        sta_lat: list[float] = []
        sta_lon: list[float] = []

        for i in range(0, len(data), 20):
            try:
                lat = int(data[i : i + 10], 2)
            except:
                lat = 0
            try:
                lon = int(data[i + 10 : i + 20], 2)
            except:
                lon = 0

            sta_lat.append(30 + lat / 100)
            sta_lon.append(120 + lon / 100)

        for i in range(len(sta_lat)):
            sta_list.append(Station(sta_lat[i], sta_lon[i], i, 1))

        if len(sta_list) > 99:
            self._station_list = sta_list

    async def __callback(self, data: str) -> None:
        mmi = await self.__mmi_bin_handler(data)

        for i in range(len(self._station_list)):
            try:
                self._station_list[i].mmi = mmi[i]
            except:
                pass

    async def __mmi_bin_handler(self, data: str) -> list[int]:
        mmi_data = []

        if len(data) > 0:
            for i in range(0, len(data), 4):
                mmi = int(data[i : i + 4], 2)
                mmi_data.append(mmi if mmi < 12 else 1)

        return mmi_data

    async def _get_MMI(self, url: str | None = None) -> None:
        url = url or BIN_PATH + f"{self.__pTime}.b"

        send_time = self.__time

        try:
            resp = await self.__client.get(url)
        except Exception as err:
            self.__logger.warn("Failed to get MMI data!")
            self.__logger.debug("Error: ", err)
            return

        recv_time = self.__time

        if resp.status != 200:
            self.__logger.warn("Invalid HTTP status code received in __get_MMI")
            return

        headers = resp.headers

        if self.__bsync:
            st = headers["ST"].replace(".", "")

            # Time-Sync
            if self._tide == self.__delay or recv_time - send_time < 100:
                self._tide = self.__time - int(st) + self.__delay

            self.__logger.debug(f"Time-Synced, Current tide is {self._tide}")

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
            if self._phase != 1:
                self._phase = 1
                self.__grid_renew = True
                self._grid_arr = []

        elif header[1] == "1" and header[2] == "0":
            if self._phase != 2:
                self.__grid_renew = True
            self._phase = 2

        elif header[1] == "1" and header[2] == "1":
            if self._phase != 3:
                self.__grid_renew = True
            self._phase = 3

        elif header[1] == "0" and header[2] == "1":
            if self._phase != 4:
                self._phase = 4

        info_str_arr = []

        for i in range(len(byte_array) - MAX_EQK_STR_LEN, len(byte_array)):
            info_str_arr.append(byte_array[i])

        if staF or len(self._station_list) < 99:
            await self._get_sta(url.replace(".b", ".s"), binary_str)
        else:
            await self.__callback(binary_str)

        eqk_data = binary_str[0 - (MAX_EQK_STR_LEN * 8 + MAX_EQK_INFO_LEN) :]

        if self._phase == 2 or self._phase == 3:
            await self.__fn_eqk_handler(eqk_data, info_str_arr)
        elif self._phase == 4:
            eqk_id = self.__parse_eqk_id(eqk_data)

            if self._eqk_event:
                self._eqk_event.earthquake_id = eqk_id

        if (self._phase == 2 or self._phase == 3) and self.__grid_renew:
            await self.__get_grid()

    async def __fn_eqk_handler(self, eqk_data: str, info_str_arr: list[str]) -> None:
        origin_lat = 30 + int(eqk_data[0:10], 2) / 100
        origin_lon = 124 + int(eqk_data[10:20], 2) / 100
        eqk_mag = int(eqk_data[20:27], 2) / 10
        eqk_depth = int(eqk_data[27:37], 2) / 10
        eqk_time = int(eqk_data[37:69], 2) * 1000
        eqk_id = "20" + str(int(eqk_data[69:95], 2)) if eqk_data else None
        eqk_max = int(eqk_data[95:99], 2)
        eqk_max_area = []
        _eqk_max_area_str = eqk_data[99:116]

        if _eqk_max_area_str != "11111111111111111":
            for i in range(17):
                if _eqk_max_area_str[i] == "1":
                    eqk_max_area.append(RA.ko[i])

        eqk_str = None
        eqk_sea = False

        if eqk_id is not None:
            loc = await self.__get_location(eqk_id, self._phase)

            if loc:
                eqk_str = loc["info_ko"]
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

    async def __get_grid(self, url: str | None = None) -> None:
        assert self._eqk_event, "No earthquake event found!"

        url = (
            url
            or BIN_PATH
            + f"{self._eqk_event.earthquake_id}{'.e' if self._phase == 2 else '.i'}"
        )

        resp = await self.__client.get(url)

        byte_array = list(resp.data)
        grid_arr = []

        for i in byte_array:
            byte_str = Utils.lpad(bin(i)[2:], 8)
            grid_arr.append(int(byte_str[0:4], 2))
            grid_arr.append(int(byte_str[4:8], 2))

        self._grid_arr = grid_arr
        self.__grid_renew = False

    def __parse_eqk_id(self, eqk_data: str) -> str | None:
        return "20" + str(int(eqk_data[69:95], 2)) if eqk_data else None


if __name__ == "__main__":
    HTTPClient()
