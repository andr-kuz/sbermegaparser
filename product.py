from bs4 import BeautifulSoup
import json

class Product:
    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.url = None
        self.price = None
        self.cashback_percent = None
        self.shop_name = None

    def as_dict(self) -> dict:
        return {
            'price': self.get_price(),
            'cashback_percent': self.get_cashback_percent(),
            'shop_name': self.get_shop_name(),
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict())

    def get_price(self) -> int | None:
        if element := self.soup.select_one('.pdp-sales-block__price-wrap_active .pdp-sales-block__price-final meta[itemprop="price"]'):
            self.price = int(element.get('content'))
        return self.price

    def get_url(self) -> str | None:
        if element := self.soup.select_one('meta[itemprop="url"]'):
            self.url = 'https://megamarket.ru' + str(element.attrs.get('content'))
        return self.url

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
