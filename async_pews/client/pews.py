import asyncio
import logging
from dataclasses import asdict
from typing import Callable

from ..model.model import EarlyWarningInfo, EarthquakeInfo
from .client import HTTPClient


class PEWSClient:
    def __init__(self) -> None:
        self.PEWSClient: HTTPClient = HTTPClient()
        self.phase = 1  # default phase

        self.__latest_eqk_time = 0
        self.__last_phase = 1
        self.__setup_logger()

    def __setup_logger(self) -> None:
        self.__logger = logging.getLogger("async_pews")

    def event(self, func: Callable) -> None:
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Must be a coroutine function!")

        if not func.__name__ in [
            "on_loop",
            "on_phase_1",
            "on_phase_2",
            "on_phase_3",
            "on_phase_4",
            "on_new_early_warning",
            "on_new_earthquake_info",
        ]:
            self.__logger.debug("Event name is not in the event list. Ignoring...")
            return

        setattr(self, func.__name__, func)

    async def start(self) -> None:
        PEWSClient = self.PEWSClient

        await PEWSClient._get_sta()
        asyncio.create_task(PEWSClient._sync_interval())

        while True:
            await asyncio.sleep(1)

            asyncio.create_task(PEWSClient._get_MMI())

            self.phase = PEWSClient._phase
            self._phase_handler(PEWSClient, self.phase)

            self.__logger.debug("Event on_loop")
            asyncio.create_task(self.on_loop())

    def _phase_handler(self, PEWSClient: HTTPClient, phase: int) -> None:
        match phase:
            case 1:
                self.__logger.debug("Event on_phase_1")
                asyncio.create_task(self.on_phase_1())

            case 2 | 3:
                if PEWSClient._eqk_event and (
                    self.__latest_eqk_time != PEWSClient._eqk_event.time
                    or (self.__last_phase == 2 and phase == 3)
                ):
                    match PEWSClient._phase:
                        case 2:
                            self.__logger.debug("Event on_new_early_warning")
                            eew_info = EarlyWarningInfo(
                                **asdict(PEWSClient._eqk_event), _client=PEWSClient
                            )
                            asyncio.create_task(self.on_new_early_warning(eew_info))
                            asyncio.create_task(self.on_phase_2(eew_info))
                        case 3:
                            self.__logger.debug("Event on_new_eqk_info")
                            eqk_info = EarthquakeInfo(
                                **asdict(PEWSClient._eqk_event), _client=PEWSClient
                            )
                            asyncio.create_task(self.on_new_earthquake_info(eqk_info))
                            asyncio.create_task(self.on_phase_3(eqk_info))

                    self.__latest_eqk_time = PEWSClient._eqk_event.time

                elif PEWSClient._eqk_event:
                    match phase:
                        case 2:
                            self.__logger.debug("Event on_phase_2")
                            eew_info = EarlyWarningInfo(
                                **asdict(PEWSClient._eqk_event), _client=PEWSClient
                            )
                            asyncio.create_task(self.on_phase_2(eew_info))
                        case 3:
                            self.__logger.debug("Event on_phase_3")
                            eqk_info = EarthquakeInfo(
                                **asdict(PEWSClient._eqk_event), _client=PEWSClient
                            )
                            asyncio.create_task(self.on_phase_3(eqk_info))
            case 4:
                self.__logger.debug("Event on_phase_4")
                asyncio.create_task(self.on_phase_4())

        self.__last_phase = phase

    async def on_new_early_warning(self, eqk_event: EarlyWarningInfo):
        ...

    async def on_new_earthquake_info(self, eqk_event: EarthquakeInfo):
        ...

    async def on_phase_1(self):
        ...

    async def on_loop(self):
        ...

    async def on_phase_2(self, eqk_event: EarlyWarningInfo):
        ...

    async def on_phase_3(self, eqk_event: EarthquakeInfo):
        ...

    async def on_phase_4(self):
        ...

    def run(self) -> None:
        asyncio.run(self.start())

    def stop(self) -> None:
        asyncio.get_event_loop().stop()


if __name__ == "__main__":
    PEWSClient().run()
