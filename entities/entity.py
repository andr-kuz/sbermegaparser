from abc import abstractmethod
from bs4 import BeautifulSoup
import json

class Entity:
    loaded_selectors: dict[str, str] = {'css': ''}
    def __init__(self, html: str):
        self._html = html
        self.soup = BeautifulSoup(html, 'html.parser')

    def __str__(self):
        return self._html

    @staticmethod
    def is_loaded() -> dict[str, str | None]:
        return {'css': None}

    @abstractmethod
    def as_dict(self) -> dict:
        pass

    def as_json(self) -> str:
        return json.dumps(self.as_dict())
