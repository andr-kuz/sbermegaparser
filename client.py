from abc import abstractmethod
from urllib.parse import quote
from product import Product
import os
import time

class ClientStalledException(Exception):
    def __init__(self):
        self.message = 'Change IP'

    def __str__(self):
        return self.message


class Client:
    def __init__(self, proxy_address: str):
        self.proxy = proxy_address
        self.cache = {}

    @abstractmethod
    def _get_data(self, url: str) -> str:
        pass

    @abstractmethod
    def test(self):
        pass

    def get_product(self, url: str) -> Product:
        if not url in self.cache:
            html = self._get_data(url)
            self._save_log(url, html)
            self._is_client_stalled(html)
            self.cache[url] = Product(html)
        return self.cache[url]

    def _is_client_stalled(self, html: str):
        stalled_text = 'Запросы с вашего устройства похожи на автоматические'
        if stalled_text in html:
            raise ClientStalledException

    def _save_log(self, url, html: str):
        name = quote(url, '')[-100:]
        path = os.path.abspath(os.path.dirname(__file__))
        with open(path + os.sep + 'temp' + os.sep + name + '.html', 'w') as f:
            f.write(html)

    def sleep(self, pause: int | float):
        time.sleep(pause)

    @abstractmethod
    def destroy(self):
        pass

    def __del__(self):
        self.destroy()
