from urllib.parse import quote
import os
from entities.entity import Entity
from platforms.platform import Platform
import time
from exceptions import ClientBrokenException


class Facade:
    """
    Do log,
    getting data from Platform.client or self cache
    reinit Clients
    """
    _current_proxy_index: int | None = None
    _proxies_rest_till: dict = {}
    _cache: dict = {}

    def __init__(
            self,
            platform: Platform,
            proxies: list[str] = [''],
            client_pause: int = 0
            ):
        self.client_pause = client_pause
        self.platform = platform
        self.proxies = proxies
        self._init_new_client()

    def _init_new_client(self) -> None:
        lowest_timer = 60
        for i, proxy in enumerate(self.proxies):
            if (
                i not in self._proxies_rest_till
                or self._proxies_rest_till[i] <= time.time()
            ):
                client_type = self.platform.client_type
                client = client_type(proxy)
                self.platform.add_client(client)
                self._current_proxy_index = i
                return
            timer = self._proxies_rest_till[i]
            lowest_timer = min(lowest_timer, timer)
        time.sleep(lowest_timer)
        return self._init_new_client()

    def _timer_current_client(self) -> None:
        self._proxies_rest_till[self._current_proxy_index] = time.time() + self.client_pause
        self._current_proxy_index = None

    def get(self, url: str) -> Entity:
        if url not in self._cache:
            try:
                data = self.platform.get(url)
                self._cache[url] = data
                self._save_log(url, data.__str__())
            except ClientBrokenException:
                self._timer_current_client()
                self._init_new_client()
                return self.get(url)
        return self._cache[url]

    def _save_log(self, url, html: str):
        name = quote(url, '')[-100:]
        path = os.path.abspath(os.path.dirname(__file__))
        with open(path + os.sep + 'temp' + os.sep + name + '.html', 'w') as f:
            f.write(html)
