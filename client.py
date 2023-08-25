from abc import abstractmethod
from urllib.parse import quote
from product import Product
import os

class ClientStalledException(Exception):
    def __init__(self):
        self.message = 'Change IP'

    def __str__(self):
        return self.message


class Client:
    url_cache = {}

    @abstractmethod
    def _get_data(self, url: str) -> str:
        pass

    def get(self, url: str) -> str:
        if not self.url_cache.get(url):
            html = self._get_data(url)
            self._save_log(url, html)
            self._is_client_stalled(html)
            self.url_cache[url] = dict(Product(html))
        return self.url_cache[url]

    def _is_client_stalled(self, html):
        stalled_text = 'Запросы с вашего устройства похожи на автоматические'
        if stalled_text in html:
            raise ClientStalledException

    def _save_log(self, url, html):
        name = quote(url, '')[-100:]
        path = os.path.abspath(os.path.dirname(__file__))
        with open(path + os.sep + 'temp' + os.sep + name + '.html', 'w') as f:
            f.write(html)
