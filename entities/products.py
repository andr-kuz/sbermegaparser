from abc import abstractmethod
from entities.entity import Entity
import json
from abc import ABCMeta


class Product(Entity, metaclass=ABCMeta):
    @abstractmethod
    def get_price(self) -> int | None:
        pass


class SberProduct(Product):
    loaded_selectors = {'css': '.prod-buy .bonus-percent'}

    def __init__(self, html: str):
        super().__init__(html)

    def as_dict(self) -> dict:
        return {
            'price': self.get_price(),
            'cashback_percent': self.get_sber_cashback_percent(),
            'shop_name': self.get_shop_name(),
            'sku': self.get_sku(),
            'offers': self.get_offers()
        }

    def get_sku(self) -> str | None:
        if element := self._soup.select_one('meta[itemprop="sku"]'):
            return element.get('content')

    def get_price(self) -> int | None:
        if element := self._soup.select_one('.sales-block-offer-price__price-final meta[itemprop="price"]'):
            return int(element.get('content'))

    def get_offers(self) -> list[dict]:
        offers = []
        if ',"offers":[{' in self._html and '}],"favoriteOffer":{' in self._html:
            offers_str = self._html.split(',"offers":[{')[1].split('}],"favoriteOffer":{')[0]
            offers_str = '[{' + offers_str + '}]'
            offers = json.loads(offers_str)
        return offers

    def get_sber_cashback_percent(self) -> int | None:
        if element := self._soup.select_one('.pdp-cashback-table__money-bonus:not(.money-bonus_grey) .bonus-percent'):
            return int(element.get_text().strip().split('%')[0])

    def get_shop_name(self) -> str | None:
        shop_name = None
        if element := self._soup.select_one('.pdp-offer-block__merchant-link'):
            shop_name = element.get_text().strip()
        elif element := self._soup.select_one('.pdp-merchant-rating-block__merchant-name'):
            shop_name = element.get_text().strip()
        return shop_name


class OzonProduct(Product):
    loaded_selectors = {'css': 'script[type="application/ld+json"]'}
    _product_data: dict = {}

    def __init__(self, html: str):
        super().__init__(html)
        self._get_product_data()

    def _get_product_data(self):
        if not self._product_data:
            if element := self._soup.select_one('script[type="application/ld+json"]'):
                self._product_data = json.loads(element.text) or {}

    def get_price(self) -> int | None:
        if price := self._product_data.get('offers', {}).get('price'):
            return int(price)

    def as_dict(self) -> dict:
        return {
            'price': self.get_price()
        }
