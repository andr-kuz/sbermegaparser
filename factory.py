from typing import Type
from client import Client
from client import ClientStalledException
from typing import Callable
import time

class Factory:
    COOLDOWN = 120
    def __init__(self, proxies: list, client_class: Type[Client]):
        self.proxies = proxies
        self.proxy_timer = dict.fromkeys(proxies, 0.0)
        self.client_class = client_class
        self.client = self._init_client()

    def _init_client(self) -> Client:
        proxy = self._get_free_proxy()
        return self.client_class(proxy)

    def _destroy_client(self, client: Client):
        self._set_proxy_timeout(client.proxy)
        client.destroy()

    def run(self, client_method: Callable, *args, **kwargs):
        while True:
            try:
                return client_method(self.client, *args, **kwargs)
            except ClientStalledException:
                self._destroy_client(self.client)
                self.client = self._init_client()

    def _set_proxy_timeout(self, proxy: str):
        self.proxy_timer[proxy] = time.time() + Factory.COOLDOWN

    def _get_free_proxy(self) -> str:
        while True:
            for proxy, timeout in self.proxy_timer.items():
                if time.time() > timeout:
                    return proxy
            time.sleep(1)
