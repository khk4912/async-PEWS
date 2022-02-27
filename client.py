import asyncio
import datetime
import logging
from time import time
from urllib.parse import quote, unquote

from conn import HTTP
from constant import (
    BIN_PATH,
    DELAY,
    HEADER_LEN,
    LOGGING_FORMAT,
    MAX_EQK_INFO_LEN,
    MAX_EQK_STR_LEN,
    RA,
    SYNC_PEROID,
    TIDE,
    TZ_MSEC,
)
from model import Station


class PEWSClient:
    def __init__(self) -> None:
        self._tide = TIDE
        self._TZ_MSEC = TZ_MSEC
        self._phase = 1
        self._bSync = True

        self.origin_lat = 37.51
        self.origin_lon = 126.94
        self.latest_eqk_time = 0
        self.eqk_time = 0
        self.eqk_mag = 0
        self.eqk_dep = 0
        self.eqk_str = ""
        self.eqk_info_str = ""
        self.eqk_time_str = ""
        self.eqk_max = 1
        self.eqk_max_area = []
        self.eqk_sea = False

        self.sta_list: list[Station] = []

        self._logger = logging.getLogger("PEWSClient")
        self._stream_handler = logging.StreamHandler()
        self._stream_handler.setFormatter(LOGGING_FORMAT)
        self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(self._stream_handler)

    @property
    def _time(self) -> int:
        return int(time() * 1000)

    @property
    def _pTime(self) -> str:
        return datetime.datetime.fromtimestamp(
            (self._time - self._tide - self._TZ_MSEC) // 1000
        ).strftime("%Y%m%d%H%M%S")

    def _fn_lpad(self, string: str, _len: int) -> str:
        while len(string) < _len:
            string = "0" + string
        return string

    def _fn_sta_bin_handler(self, data: str):
        new_sta_list = []
        sta_lat_arr = []
        sta_lon_arr = []

        for i in range(0, len(data), 20):
            sta_lat_arr.append(30 + int(data[i : i + 10], 2) / 100)
            sta_lon_arr.append(120 + int(data[i + 10 : i + 20], 2) / 100)

        for i in range(len(sta_lat_arr)):
            new_sta_list.append(Station(sta_lat_arr[i], sta_lon_arr[i], i))

        if len(new_sta_list) > 99:
            self.sta_list = new_sta_list

    def _mmi_bin_handler(self, data: str):
        mmi_data = []
        for i in range(0, len(data), 4):
            mmi_data.append(int(data[i : i + 4], 2))

        return mmi_data

    def _eqk_handler(self, data: str, buffer: list[int]):
        self._origin_lat = 30 + int(data[0:10], 2) / 100
        self._origin_lon = 120 + int(data[10:20], 2) / 100
        self.eqk_mag = int(data[20:27], 2) / 10
        self.eqk_dep = int(data[27:37], 2) / 10
        self.eqk_time = int(str(int(data[37:69], 2)) + "000")
        self.eqk_id = self._parse_eqk_id(data)
        self.eqk_max = int(data[95:99], 2)
        self.eqk_max_area = []

        eqk_max_area_str = data[99:116]

        if eqk_max_area_str != "11111111111111111":
            for i in range(17):
                if eqk_max_area_str[i] == "1":
                    self.eqk_max_area.append(RA[i])
        else:
            self.eqk_max_area.append("-")

        eqk_str = unquote(
            quote("".join([chr(x) for x in buffer]), encoding="raw_unicode_escape")
        ).strip()
        eqk_sea = eqk_str.find("해역") != -1

    def _parse_eqk_id(self, data: str) -> str:
        return "" if not data else "20" + str(int(data[69:95], 2))

    def _callback(self, data: str):
        mmi_data = self._mmi_bin_handler(data)
        for i in range(len(self.sta_list)):
            self.sta_list[i].mmi = mmi_data[i]

    async def _sync_interval(self):
        while True:
            await asyncio.sleep(SYNC_PEROID)
            self._bSync = True

    async def get_sta(self, url: str, data: str | None = None):
        binary_str = ""

        array_buffer, _ = await HTTP.get(url)
        byte_array = list(array_buffer)

        for i in byte_array:
            binary_str += self._fn_lpad(str(bin(i)[2:]), 8)

        self._fn_sta_bin_handler(binary_str)

        if data is not None:
            self._callback(data)

        self._logger.debug(f"{url.split('/')[-1]}")
        self._logger.info("측정소 목록 정보 수신 완료")

    async def get_MMI(self, url: str):
        send_time = self._time
        array_buffer, headers = await HTTP.get(url)
        byte_array = list(array_buffer)

        if self._bSync:
            receive_time = self._time
            dTime = int(headers["ST"].replace(".", ""))
            if self._tide == DELAY or receive_time - send_time < 100:
                self._tide = self._time - dTime + DELAY
            self._logger.info(f"서버 시간과 동기화됨 ({headers['Date']})")
            self._logger.info(f"현재 시간차: {self._tide}ms")

            self._bSync = False

        header = ""
        binary_str = ""

        for i in range(HEADER_LEN):
            header += self._fn_lpad(bin(byte_array[i])[2:], 8)
        for i in range(HEADER_LEN, len(byte_array)):
            binary_str += self._fn_lpad(bin(byte_array[i])[2:], 8)

        staF = header[0] == "1"
        if header[1] == "0" and header[2] == "0":
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

        if staF or len(self.sta_list) < 99:
            await self.get_sta(f"{url}.s", binary_str)
        else:
            self._callback(binary_str)

        eqk_data = binary_str[0 - (MAX_EQK_STR_LEN * 8 + MAX_EQK_INFO_LEN) :]
        if self._phase == 2 or self._phase == 3:
            self._eqk_handler(eqk_data, info_str_arr)
        elif self._phase == 4:
            self._parse_eqk_id(eqk_data)

        self._logger.debug(f"{url.split('/')[-1]}")

    async def run(self):
        await self.get_sta(f"{BIN_PATH}{self._pTime}.s")
        await self.get_MMI(f"{BIN_PATH}{self._pTime}.b")
        asyncio.create_task(self._sync_interval())

        while True:
            cTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            if cTime != self._pTime:
                await self.get_MMI(f"{BIN_PATH}{cTime}.b")

            if self._phase == 2:
                pass

            await asyncio.sleep(1)


a = PEWSClient()

asyncio.run(a.run())
