import re
from typing import Type
from entities.entity import Entity
from clients.client import Client
from exceptions import ClientBrokenException
from abc import ABCMeta
import time


class Platform(metaclass=ABCMeta):
    client_type = Client
    _client: Client | None = None
    _entities_regex: dict[str, type[Entity]]
    _stalled_text: str = ''
    _rest_time: int = 5
    _timer_end = 0

    def __init__(self, timer: int = 0):
        self._rest_time = timer or self._rest_time

    def add_client(self, client: Client):
        self._client = client

    def _destroy_client(self):
        if self._client:
            self._client.__del__()
        self._client = None

    def _wait_timer(self):
        timer_left = self._timer_end - time.time()
        if timer_left > 0:
            time.sleep(timer_left)

    def _set_timer(self):
        self._timer_end = self._rest_time + time.time()

    def get(self, url: str) -> Entity:
        if not issubclass(type(self._client), Client):
            raise Exception('You need to pass Client to add_client() first')
        self._wait_timer()
        entity = self._detect_entity_by_url(url)
        data = self._client.get(url, entity.loaded_selectors.get('css'))
        if self._is_client_broken(data):
            self._destroy_client()
            raise ClientBrokenException
        self._set_timer()
        return entity(data)

    def _detect_entity_by_url(self, url: str) -> Type[Entity]:
        for regex, entity in self._entities_regex.items():
            pattern = re.compile(regex)
            if pattern.match(url):
                return entity
        raise Exception('No entity found')

    def _is_client_broken(self, page_data: str) -> bool | None:
        if self._stalled_text and self._stalled_text in page_data:
            return True
