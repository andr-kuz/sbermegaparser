from clients.client import Client
from exceptions import ClientBrokenException
import time
from abc import abstractmethod


class Platform:
    client: Client
    def __init__(self, timer: int = 0, proxy_timer: int = 0):
        self.rest_time = timer
        self.proxy_timer = proxy_timer
        self.timer_end = 0
        self.client = Platform.client

    def add_client(self, client: Client):
        self.client = client

    def _destroy_client(self):
        self.client.destroy()
        self.client = Platform.client

    def _wait_timer(self):
        timer_left = self.timer_end - time.time()
        if timer_left > 0:
            time.sleep(timer_left)

    def _set_timer(self):
        self.timer_end = self.rest_time + time.time()

    def _get(self, url: str, find_css_on_page: str = ''):
        if not isinstance(self.client, type(Client)):
            raise Exception('You need to pass Client to add_client() first')
        self._wait_timer()
        data = self.client.get(url, find_css_on_page)
        if self._is_client_broken(data):
            self._destroy_client()
            raise ClientBrokenException
        self._set_timer()
        return data

    @abstractmethod
    def _is_client_broken(self, page_data: str):
        pass
