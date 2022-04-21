# async-PEWS

대한민국 기상청에서 제공하는 [사용자 맞춤형 지진정보서비스](https://www.weather.go.kr/pews/)의 비동기 파이썬 클라이언트

## Usage

```python
from async_pews import PEWSClient
from async_pews.model import EEWInfo, EqkInfo

pews = PEWSClient()


@pews.event
async def on_loop():
    # 매 요청마다 실행되는 이벤트
    ...


@pews.event
async def on_new_eew_info(eew_info: EEWInfo):
    # 새로운 조기경보가 발표되는 순간(phase 2)에 발생하는 이벤트
    print("## 새로운 조기경보 발생! ##")
    print(f"{eew_info.eqk_str}에서 추정규모 {eew_info.mag}의 정보 수신!")
    ...

    # === EEWInfo Example ===
    #
    # EEWInfo(lat=33.15,
    #         lon=122.24,
    #         mag=5.3,
    #         dep=0.0,
    #         time=datetime.datetime(2021, 12, 14, 8, 19, 16),
    #         max_intensity=6,
    #         max_area=['제주'],
    #         sea=True,
    #         eqk_str='제주 서귀포시 서남서쪽 32km 해역')


@pews.event
async def on_phase_2(eew_info: EEWInfo):
    ...

@pews.event
async def on_phase_3(eqk_info: EqkInfo):
    ...


pews.start()
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
