from bs4 import BeautifulSoup

class Entity:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.price = None

    @staticmethod
    def is_loaded() -> dict[str, str | None]:
        return {'css': None}
