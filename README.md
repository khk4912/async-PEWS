# async-PEWS

![discord.py version](https://img.shields.io/badge/Python-%3E%3D%203.10-blue?style=for-the-badge&logo=python)  
대한민국 기상청에서 제공하는 [사용자 맞춤형 지진정보서비스](https://www.weather.go.kr/pews/)의 Python 비동기 클라이언트

## Usage

```py
from async_pews import PEWSClient, EarlyWarningInfo, EarthquakeInfo

pews = PEWSClient()

@pews.event
async def on_new_early_warning(event: EarlyWarningInfo):
    """
    새로운 조기경보가 발표되는 순간(phase 2)에 한번만 실행되는 이벤트
    """

@pews.event
async def on_new_earthquake_info(event: EarthquakeInfo):
    """
    새로운 지진정보가 발표되는 순간(phase 3)에 한번만 실행되는 이벤트
    """


pews.start()
```
