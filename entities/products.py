from abc import abstractmethod
from entities.entity import Entity
import json

class Product(Entity):
    price = None
    @abstractmethod
    def get_price(self):
        pass


class SberProduct(Product):
    loaded_selectors = {'css': '.prod-buy .bonus-percent'}
    def __init__(self, html: str):
        super().__init__(html)
        self.url = None
        self.cashback_percent = None
        self.shop_name = None

    def as_dict(self) -> dict:
        return {
            'price': self.get_price(),
            'cashback_percent': self.get_cashback_percent(),
            'shop_name': self.get_shop_name(),
            'offers': self.get_offers()
        }

    def get_price(self) -> int | None:
        if element := self.soup.select_one('.prod-buy meta[itemprop="price"]'):
            self.price = int(element.get('content'))
        return self.price

    def get_offers(self) -> list[dict]:
        offers = []
        if ',"offers":[{' in self._html and '}],"favoriteOffer":{' in self._html:
            offers_str = self._html.split(',"offers":[{')[1].split('}],"favoriteOffer":{')[0]
            offers_str = '[{'+ offers_str +'}]'
            offers = json.loads(offers_str)
        return offers

    def get_cashback_percent(self) -> int | None:
        if element := self.soup.select_one('.pdp-cashback-table__money-bonus:not(.money-bonus_grey) .bonus-percent'):
            self.cashback_percent = int(element.get_text().strip().split('%')[0])
        return self.cashback_percent

    def get_shop_name(self) -> str | None:
        if element := self.soup.select_one('.pdp-offer-block__merchant-link'):
            self.shop_name = element.get_text().strip()
        elif element := self.soup.select_one('.pdp-merchant-rating-block__merchant-name'):
            self.shop_name = element.get_text().strip()
        return self.shop_name

class OzonProduct(Product):
    loaded_selectors = {'css': 'script[type="application/ld+json"]'}
    product_data: dict = {}

    def __init__(self, html: str):
        super().__init__(html)
        self._get_product_data()

    def _get_product_data(self):
        if not self.product_data:
            if element := self.soup.select_one('script[type="application/ld+json"]'):
                self.product_data = json.loads(element.text) or {}

    def get_price(self) -> int | None:
        if price := self.product_data.get('offers', {}).get('price'):
            return int(price)

    def as_dict(self) -> dict:
        return {
            'price': self.get_price()
        }
