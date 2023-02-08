from datetime import datetime
from typing import NamedTuple

from .sim import SimulationPEWS


class SimulationDataset(NamedTuple):
    JEJU = SimulationPEWS(
        2021007178,
        datetime(2021, 12, 14, 17, 19, 9),
        datetime(2021, 12, 14, 17, 27, 23),
    )

    POHANG = SimulationPEWS(
        2017000407,
        datetime(2017, 11, 15, 14, 29, 21),
        datetime(2017, 11, 15, 14, 34, 20),
    )

    GYEONGJU = SimulationPEWS(
        2016000291,
        datetime(2016, 9, 12, 20, 32, 44),
        datetime(2016, 9, 12, 20, 37, 43),
    )
