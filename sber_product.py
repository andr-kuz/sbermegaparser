from bs4 import BeautifulSoup
import json

class SberProduct:
    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def __str__(self):
        return json.dumps({
            'url': self.get_url(),
            'price': self.get_price(),
            'cashback_percent': self.get_cashback_percent(),
            'shop_name': self.get_shop_name(),
        })

    def get_price(self, raw = False) -> int | str | None:
        result = None
        if element := self.soup.select_one('.pdp-sales-block__price-wrap_active .pdp-sales-block__price-final meta[itemprop="price"]'):
            result = element.get('content')
        return result

    def get_url(self) -> str | None:
        if element := self.soup.select_one('meta[itemprop="url"]'):
            return 'https://megamarket.ru' + str(element.attrs.get('content'))

    def get_cashback_percent(self, raw = False) -> int | str | None:
        result = None
        if element := self.soup.select_one('.pdp-sales-block__bonus_active .bonus-percent'):
            result = element.get_text().strip()
            if not raw and result:
                result = int(result.split('%')[0])
        return result

    def get_shop_name(self, raw = False) -> int | str | None:
        result = None
        if element := self.soup.select_one('.pdp-offer-block__merchant-link'):
            if result := element.get_text().strip():
                return result
        return result
