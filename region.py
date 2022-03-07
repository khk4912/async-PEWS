# TODO
import asyncio
from client import PEWSClient


class TEST(PEWSClient):
    def __init__(self) -> None:
        super().__init__()

    async def on_new_eew_info(self, test):
        print(test)


a = TEST()
asyncio.run(a._looper())
