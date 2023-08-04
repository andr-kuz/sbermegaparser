from client import Client
from sber_product import SberProduct
from selenium.webdriver.firefox.webdriver import WebDriver


class SberScraper:
    def __init__(self, driver: WebDriver):
        self.driver = Client(driver)
        self.url_cache = {}

    def get_product(self, url) -> SberProduct:
        if not self.url_cache.get(url):
            html = self.driver.get(url)
            product = SberProduct(html)
            self.url_cache[url] = product
        return self.url_cache[url]
