from abc import abstractmethod
from bs4 import BeautifulSoup
import json

class Entity:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.price = None

    @staticmethod
    def is_loaded() -> dict[str, str | None]:
        return {'css': None}

    @abstractmethod
    def as_dict(self) -> dict:
        pass

    def as_json(self) -> str:
        return json.dumps(self.as_dict())
