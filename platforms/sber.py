from entities.products import SberProduct
from platforms.platform import Platform

class Sber(Platform):
    stalled_text = 'Запросы с вашего устройства похожи на автоматические'
    product_fully_loaded_css = '.pdp-cashback-table__money-bonus:not(.money-bonus_grey) .bonus-percent'

    def _is_client_broken(self, page_data: str) -> bool | None:
        if Sber.stalled_text in page_data:
            return True

    def get_product(self, url: str) -> SberProduct:
        data = self._get(url, Sber.product_fully_loaded_css)
        return SberProduct(data)
