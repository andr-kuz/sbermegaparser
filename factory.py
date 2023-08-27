from typing import Type
from abc import abstractmethod
from client import Client
from client import ClientStalledException
import time

class Factory:
    COOLDOWN = 120
    def __init__(self, proxies: list, client_class: Type[Client]):
        self.proxies = proxies
        self.proxy_timer = dict.fromkeys(self.proxies, 0.0)
        self.client_class = client_class
        self.client = self._init_client()

    @abstractmethod
    def _init_client(self) -> Type[Client]:
        proxy = self._get_free_proxy()
        return self.client_class(proxy)

    def run(self, command: str, *args, **kwargs):
        while True:
            try:
                method = getattr(self.client, command)
                data = method(*args, **kwargs)
                return data
            except ClientStalledException:
                proxy = getattr(self.client, 'proxy')
                getattr(self.client, 'destroy')()
                self._set_proxy_timeout(proxy)
                self.client = self._init_client()

    def _set_proxy_timeout(self, proxy: str):
        self.proxy_timer[proxy] = time.time() + Factory.COOLDOWN

    def _get_free_proxy(self) -> str:
        while True:
            for proxy, timeout in self.proxy_timer.items():
                if time.time() > timeout:
                    return proxy
            time.sleep(1)
