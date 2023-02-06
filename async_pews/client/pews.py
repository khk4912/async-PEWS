import asyncio

from async_pews.model.model import EarthquakeEvent

from .client import HTTPClient


class PEWS:
    def __init__(self) -> None:
        self.__latest_eqk_time = 0
        self.phase: int = 1

    async def start(self) -> None:
        PEWSClient = HTTPClient()

        await PEWSClient._get_sta()

        while True:
            await asyncio.sleep(1)
            asyncio.create_task(PEWSClient._get_MMI())

            self.phase = PEWSClient._phase

            match (phase := self.phase):
                case 2 | 3:
                    assert PEWSClient._eqk_event

                    if self.__latest_eqk_time != PEWSClient._eqk_event.time:
                        match PEWSClient._phase:
                            case 2:
                                asyncio.create_task(
                                    self.on_new_early_warning(PEWSClient._eqk_event)
                                )
                                asyncio.create_task(
                                    self.on_phase_2(PEWSClient._eqk_event)
                                )
                            case 3:
                                asyncio.create_task(
                                    self.on_new_earthquake_info(PEWSClient._eqk_event)
                                )
                                asyncio.create_task(
                                    self.on_phase_3(PEWSClient._eqk_event)
                                )

                        self.__latest_eqk_time = PEWSClient._eqk_event.time

                    else:
                        match phase:
                            case 2:
                                asyncio.create_task(
                                    self.on_phase_2(PEWSClient._eqk_event)
                                )
                            case 3:
                                asyncio.create_task(
                                    self.on_phase_3(PEWSClient._eqk_event)
                                )
                            case 4:
                                asyncio.create_task(self.on_phase_4())

    async def on_new_early_warning(self, eqk_event: EarthquakeEvent):
        ...

    async def on_new_earthquake_info(self, eqk_event: EarthquakeEvent):
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
