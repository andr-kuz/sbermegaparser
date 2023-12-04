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
        }

    def get_price(self) -> int | None:
        if element := self.soup.select_one('.prod-buy meta[itemprop="price"]'):
            self.price = int(element.get('content'))
        return self.price

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
    loaded_selectors = {'css': '[id^="state-webPrice-"]'}
    product_data: dict = {}

    def get_price(self) -> int | None:
        if not self.product_data:
            if element := self.soup.select_one('[id^="state-webPrice-"][data-state]'):
                self.product_data = json.loads(element.get('data-state')) or {}
        return self.product_data.get('price', 0)

    def as_dict(self) -> dict:
        return {
            'price': self.get_price()
        }
