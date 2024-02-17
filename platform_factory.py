from typing import Type
from platforms import Ozon, Sber, Platform
import re


class PlatformFactory:
    _platforms_regex = {
        'https://megamarket.ru': Sber,
        'https://www.ozon.ru': Ozon
    }

    @staticmethod
    def detect_platform(url: str) -> Type[Platform]:
        for regex, platform in PlatformFactory._platforms_regex.items():
            pattern = re.compile(regex)
            if pattern.match(url):
                return platform
        raise Exception('No platform detected')
