import threading
import eel

from async_pews import PEWSClient


pews = PEWSClient()

eel.init("web")


def pews_starter() -> None:
    pews.start()


@eel.expose
def get_station() -> list[tuple[int | None, float, float]]:
    return [(x.mmi, x.lat, x.lon) for x in pews.sta_list]


thread = threading.Thread(target=pews_starter)
thread.start()

print(pews.sta_list)

eel.start("index.html")
