from abc import abstractmethod
from bs4 import BeautifulSoup
import json
from abc import ABCMeta


class Entity(metaclass=ABCMeta):
    loaded_selectors: dict[str, str] = {'css': ''}
    _soup: BeautifulSoup

    def __init__(self, html: str):
        self._html = html
        self._soup = BeautifulSoup(html, 'html.parser')

    def __str__(self):
        return self._html

    @abstractmethod
    def as_dict(self) -> dict:
        pass

    def as_json(self) -> str:
        return json.dumps(self.as_dict())
