from abc import abstractmethod
from client import Client
from client import ClientStalledException
import time

class Fabrique:
    COOLDOWN = 120
    def __init__(self, proxies: list):
        self.proxies = proxies
        self.proxy_timer = dict.fromkeys(self.proxies, 0.0)
        self.proxy = self.get_free_proxy()
        self.client = self._init_client(self.proxy)

    @abstractmethod
    def _init_client(self, proxy: str) -> Client:
        pass

    def run(self, command: str, *args, **kwargs):
        while True:
            try:
                method = getattr(self.client, command)
                data = method(*args, **kwargs)
                return data
            except ClientStalledException:
                self.client.destroy()
                self.set_proxy_timeout(self.proxy)
                self.proxy = self.get_free_proxy()
                self.client = self._init_client(self.proxy)

    def set_proxy_timeout(self, proxy: str):
        self.proxy_timer[proxy] = time.time() + Fabrique.COOLDOWN

    def get_free_proxy(self) -> str:
        while True:
            for proxy, timeout in self.proxy_timer.items():
                if time.time() > timeout:
                    return proxy
            time.sleep(1)
