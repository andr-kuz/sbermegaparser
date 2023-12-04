from typing import Callable, Type
from urllib.parse import quote
import os
from platforms.platform import Platform
from platforms.sber import Sber
from platforms.sber import Ozon
import time
from exceptions import ClientBrokenException
import re

class Facade:
    """
    Do log,
    getting data from Platform.client or self cache
    rotate Clients
    """
    _current_client_index: int | None = None
    _clients_rest_till: dict = {}
    _cache: dict = {}
    _platforms_regex = {
        'https://megamarket.ru': Sber,
        'ozon.ru': Ozon
    }
    def __init__(self, platform: Platform, packed_clients: list[Callable], client_timer: int = 0):
        self._client_timer = client_timer
        self._platform = platform
        self._clients = packed_clients
        self._init_new_client()

    def _init_new_client(self) -> None:
        lowest_timer = 60
        for i, packed_client in enumerate(self._clients):
            if i not in self._clients_rest_till or self._clients_rest_till[i] <= time.time():
                client = packed_client()
                self._platform.add_client(client)
                self._current_client_index = i
                return
            timer = self._clients_rest_till[i]
            lowest_timer = min(lowest_timer, timer)
        time.sleep(lowest_timer)
        return self._init_new_client()

    def _timer_current_client(self) -> None:
        self._clients_rest_till[self._current_client_index] = time.time() + self._client_timer
        self._current_client_index = None

    def get(self, url: str):
        if not url in self._cache:
            try:
                data = self._platform.get(url)
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

    @staticmethod
    def detect_platform_by_url(url: str) -> Type[Platform]:
        for regex, platform in Facade._platforms_regex.items():
            pattern = re.compile(regex)
            if pattern.match(url):
                return platform
        raise Exception('No platform detected')
