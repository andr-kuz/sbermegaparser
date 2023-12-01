from entities.products import SberProduct
from platforms.platform import Platform

class Sber(Platform):
    stalled_text = 'Запросы с вашего устройства похожи на автоматические'
    entities_regex = {
        'https://megamarket.ru/catalog/details/[a-zA-Z0-9-]+/?$': SberProduct
    }

    def _is_client_broken(self, page_data: str) -> bool | None:
        if Sber.stalled_text in page_data:
            return True
