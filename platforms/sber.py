from entities import SberProduct
from platforms.platform import Platform
from clients import Firefox


class Sber(Platform):
    _stalled_text = 'Запросы с вашего устройства похожи на автоматические'
    _entities_regex = {
        'https://megamarket.ru/catalog/details/[a-zA-Z0-9-]+/?$': SberProduct
    }
    _rest_time = 5
    client_type = Firefox
