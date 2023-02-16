# async-PEWS

![discord.py version](https://img.shields.io/badge/Python-%3E%3D%203.10-blue?style=for-the-badge&logo=python)  
대한민국 기상청에서 제공하는 [사용자 맞춤형 지진정보서비스](https://www.weather.go.kr/pews/)의 Python 비동기 클라이언트

## Supported features

- 지진속보 / 지진정보  
  다음과 같은 정보가 제공됩니다.

  - 위·경도
  - 규모
  - 깊이
  - 발생시각
  - 해역 여부
  - 최대진도 및 그 지역
  - 특정 위·경도의 (예상)진도 및 지진파 도달 시각

- 시뮬레이션  
  기상청에서 기본으로 제공하는 다음 지진들의 요청 정보가 저장되어 있습니다.  
  해당 지진들의 정보를 통해 지진 발생시 이벤트 핸들러의 동작을 시험해볼 수 있습니다.

  - 제주 지진 (2021-12-14 17:19:14, 규모 4.9) -> `async_pews.SimulationDataset.JEJU`
  - 포항 지진 (2017-11-15 14:29:31, 규모 5.4) -> `async_pews.SimulationDataset.POHANG`
  - 경주 지진 (2016-09-12 20:32:54, 규모 5.8) -> `async_pews.SimulationDataset.GYEONGJU`

### TODO

- ID 기반 다중 지진 핸들...?
- 특정 상황에서 phase 이벤트가 발생하지 않는 문제 해결

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
