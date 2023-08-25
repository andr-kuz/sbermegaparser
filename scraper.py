from client import Client
from product import Product
from selenium.webdriver.firefox.webdriver import WebDriver


class Scraper:
    def __init__(self, client: WebDriver):
        self.client = Client(client)
        self.url_cache = {}

    def get_product(self, url) -> Product:
        if not self.url_cache.get(url):
            html = self.client.get(url)
            product = Product(html)
            self.url_cache[url] = product
        return self.url_cache[url]
