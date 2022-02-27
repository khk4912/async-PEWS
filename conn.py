import aiohttp


class HTTP:
    @staticmethod
    async def get(url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    content = await r.content.read()
                    return content, r.headers
                else:
                    raise Exception(f"HTTP Error: {r.status}")
