import logging
from aiohttp import ClientSession

from async_pews.model.model import Response


class SessionClient:
    def __init__(self) -> None:
        self.__session: ClientSession | None = None
        self.__logger = logging.getLogger("async_pews")

    async def get(self, url) -> Response:

        if not self.__session:
            self.__session = ClientSession()
            self.__logger.debug("New session created.")

        self.__logger.debug(f"Request to {url}")

        try:
            async with self.__session.get(url) as r:
                resp = Response(r.status, await r.read(), r.headers)
        except Exception as e:
            self.__logger.warn("Failed to request!")
            self.__logger.debug("Error: ", e)
            raise e

        return resp

    async def close(self) -> None:
        if self.__session:
            await self.__session.close()
