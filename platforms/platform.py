import re
from typing import Type
from entities.entity import Entity
from clients.client import Client
from exceptions import ClientBrokenException
import time


class Platform:
    client_class = Client
    client: Client | None = None
    entities_regex: dict[str, type[Entity]]
    stalled_text: str = ''
    rest_time: int = 5
    timer_end = 0

    def __init__(self, timer: int = 0):
        self.rest_time = timer or self.rest_time

    def add_client(self, client: Client):
        self.client = client

    def _destroy_client(self):
        if self.client:
            self.client.__del__()
        self.client = None

    def _wait_timer(self):
        timer_left = self.timer_end - time.time()
        if timer_left > 0:
            time.sleep(timer_left)

    def _set_timer(self):
        self.timer_end = self.rest_time + time.time()

    def get(self, url: str) -> Entity:
        if not issubclass(type(self.client), Client):
            raise Exception('You need to pass Client to add_client() first')
        self._wait_timer()
        entity = self._detect_entity_by_url(url)
        data = self.client.get(url, entity.loaded_selectors.get('css'))
        if self._is_client_broken(data):
            self._destroy_client()
            raise ClientBrokenException
        self._set_timer()
        return entity(data)

    def _detect_entity_by_url(self, url: str) -> Type[Entity]:
        for regex, entity in self.entities_regex.items():
            pattern = re.compile(regex)
            if pattern.match(url):
                return entity
        raise Exception('No entity found')

    def _is_client_broken(self, page_data: str) -> bool | None:
        if self.stalled_text and self.stalled_text in page_data:
            return True
