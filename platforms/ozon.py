from platforms.platform import Platform
from entities import OzonProduct
from clients import Firefox


class Ozon(Platform):
    _stalled_text = '<h1>Доступ ограничен</h1>'
    _entities_regex = {
        'https://www.ozon.ru/product/[a-zA-Z0-9-]+?/': OzonProduct
    }
    _rest_time = 8
    client_type = Firefox
