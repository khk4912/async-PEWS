import logging
import asyncio

from ..model.model import EarthquakeEvent
from .client import HTTPClient


class PEWS:
    def __init__(self) -> None:
        self.__latest_eqk_time = 0
        self.__setup_logger()

    def __setup_logger(self) -> None:
        self.__logger = logging.getLogger("async_pews")

    async def start(self) -> None:
        PEWSClient = HTTPClient()

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
                if (
                    PEWSClient._eqk_event
                    and self.__latest_eqk_time != PEWSClient._eqk_event.time
                ):
                    match PEWSClient._phase:
                        case 2:
                            self.__logger.debug("Event on_new_early_warning")
                            asyncio.create_task(
                                self.on_new_early_warning(PEWSClient._eqk_event)
                            )
                            asyncio.create_task(self.on_phase_2(PEWSClient._eqk_event))
                        case 3:
                            self.__logger.debug("Event on_new_eqk_info")
                            asyncio.create_task(
                                self.on_new_earthquake_info(PEWSClient._eqk_event)
                            )
                            asyncio.create_task(self.on_phase_3(PEWSClient._eqk_event))

                    self.__latest_eqk_time = PEWSClient._eqk_event.time

                elif PEWSClient._eqk_event:
                    match phase:
                        case 2:
                            self.__logger.debug("Event on_phase_2")
                            asyncio.create_task(self.on_phase_2(PEWSClient._eqk_event))
                        case 3:
                            self.__logger.debug("Event on_phase_3")
                            asyncio.create_task(self.on_phase_3(PEWSClient._eqk_event))
                        case 4:
                            self.__logger.debug("Event on_phase_4")
                            asyncio.create_task(self.on_phase_4())

    async def on_new_early_warning(self, eqk_event: EarthquakeEvent):
        ...

    async def on_new_earthquake_info(self, eqk_event: EarthquakeEvent):
        ...

    async def on_phase_1(self):
        ...

    async def on_loop(self):
        ...

    async def on_phase_2(self, eqk_event: EarthquakeEvent):
        ...

    async def on_phase_3(self, eqk_event: EarthquakeEvent):
        ...

    async def on_phase_4(self):
        ...

    def run(self) -> None:
        asyncio.run(self.start())


if __name__ == "__main__":
    PEWS().run()
