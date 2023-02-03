from aiohttp import ClientSession


class HTTPClient:
    def __init__(self) -> None:
        self.__session = ClientSession()

    async def get(self, url: str) -> str:
        ...
