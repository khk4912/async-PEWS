import discord
import asyncio


from async_pews import (
    SimulationPEWS,
    PEWSClient,
    EarlyWarningInfo,
    EarthquakeInfo,
)

pews = PEWSClient()

CHANNEL_ID = 1  # 경고할 텍스트 채널 ID
TOKEN = ""  # 봇의 토큰


class EEWWarningBot(discord.Client):
    def __init__(self, PEWSClient: PEWSClient | SimulationPEWS) -> None:
        super().__init__(intents=discord.Intents.default())
        self.pews = PEWSClient

    async def on_ready(self) -> None:
        self.channel = await self.fetch_channel(CHANNEL_ID)
        asyncio.create_task(self.pews.start())
        print(f"Logged in as {self.user}")

    async def early_warning(self, event: EarlyWarningInfo) -> None:
        channel = self.channel
        assert isinstance(channel, discord.TextChannel)

        mmi = ["", "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ+"]

        embed = (
            discord.Embed(colour=discord.Colour.red(), title="⚠️ 지진 속보", description="")
            .add_field(
                name="발생시각",
                value=f"<t:{int(event.time.timestamp())}:F>",
                inline=False,
            )
            .add_field(
                name="발생위치",
                value=f"{event.earthquake_str}",
                inline=False,
            )
            .add_field(name="진원의 깊이", value=f"{event.depth}km", inline=False)
            .add_field(name="추정규모", value=f"{event.magnitude}", inline=True)
            .add_field(
                name="예상최대진도",
                value=f"{mmi[event.max_intensity]} ({', '.join(event.max_intensity_area)})",
                inline=True,
            )
            .add_field(
                name="주요지역 도달까지 남은 시간",
                value=f"서울: <t:{int(event.estimated_arrival_time(37.33, 126.58).timestamp())}:R>\n부산: <t:{int(event.estimated_arrival_time(35.10, 129.04).timestamp())}:R>\n대전: <t:{int(event.estimated_arrival_time(36.21, 127.23).timestamp())}:R>",
                inline=False,
            )
        )

        await channel.send(embed=embed)

    async def earthquake_info(self, event: EarthquakeInfo) -> None:
        channel = self.channel
        assert isinstance(channel, discord.TextChannel)

        mmi = ["", "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ+"]

        embed = (
            discord.Embed(colour=discord.Colour.blue(), title="📝 지진 정보", description="")
            .add_field(
                name="발생시각",
                value=f"<t:{int(event.time.timestamp())}:F>",
                inline=False,
            )
            .add_field(
                name="발생위치",
                value=f"{event.earthquake_str}",
                inline=False,
            )
            .add_field(name="진원의 깊이", value=f"{event.depth}km", inline=False)
            .add_field(name="규모", value=f"{event.magnitude}", inline=True)
            .add_field(
                name="최대진도",
                value=f"{mmi[event.max_intensity]} ({', '.join(event.max_intensity_area)})",
                inline=True,
            )
        )
        await channel.send(embed=embed)


@pews.event
async def on_new_early_warning(eqk_event: EarlyWarningInfo) -> None:
    await bot.early_warning(eqk_event)


@pews.event
async def on_new_earthquake_info(eqk_event: EarthquakeInfo) -> None:
    await bot.earthquake_info(eqk_event)


bot = EEWWarningBot(pews)
bot.run(TOKEN)
