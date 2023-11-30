from typing_extensions import Type
from urllib.parse import quote
import os
from platforms.platform import Platform
from clients.client import Client

class Facade:
    """
    Do log,
    getting data from Platform.client or self cache
    rotate Clients
    """
    def __init__(self, platform: Type[Platform], client: Type[Client], args_and_kwargs: tuple[list, dict]):
        pass

    def _save_log(self, url, html: str):
        name = quote(url, '')[-100:]
        path = os.path.abspath(os.path.dirname(__file__))
        with open(path + os.sep + 'temp' + os.sep + name + '.html', 'w') as f:
            f.write(html)
