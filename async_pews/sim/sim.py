import asyncio
from datetime import datetime, timedelta

from ..client.CONSTANT import BIN_PATH
from ..client.client import HTTPClient
from ..client.pews import PEWS


class SimulationPEWS(PEWS):
    def __init__(self, eqk_id: int, start_time: datetime, end_time: datetime) -> None:
        super().__init__()
        self.__eqk_id = eqk_id
        self.__start_time = start_time - timedelta(hours=9)
        self.__cur_time = self.__start_time
        self.__end_time = end_time - timedelta(hours=9)

    def increase_time(self):
        self.__cur_time += timedelta(seconds=1)

    async def start(self) -> None:
        PEWSClient_Sim = HTTPClient(sim=True)

        await PEWSClient_Sim._get_sta(
            f"{BIN_PATH}{self.__eqk_id}/{self.__start_time.strftime('%Y%m%d%H%M%S')}.s"
        )

        while True:
            await asyncio.sleep(1)
            self.increase_time()

            if self.__cur_time > self.__end_time:
                break

            asyncio.create_task(
                PEWSClient_Sim._get_MMI(
                    f"{BIN_PATH}{self.__eqk_id}/{self.__cur_time.strftime('%Y%m%d%H%M%S')}.b"
                )
            )
            self.phase = PEWSClient_Sim._phase
            self._phase_handler(PEWSClient_Sim, self.phase)
