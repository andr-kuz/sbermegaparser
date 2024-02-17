from playwright.sync_api import sync_playwright
from clients.client import Client
from playwright._impl._errors import TimeoutError
import atexit


class Playwright(Client):
    def __init__(self, proxy_address: str):
        atexit.register(self.__del__)
        self.proxy = proxy_address
        self.playwright = sync_playwright().start()
        self.driver = self.playwright.firefox.launch(
            headless=True,
        )

    def get(self, url: str, find_css_on_page: str | None = '') -> str:
        page = self.driver.new_page()
        page.goto(url)
        if find_css_on_page:
            try:
                page.wait_for_selector(find_css_on_page, timeout=15000)
            except TimeoutError:
                pass
        data = page.content()
        page.close()
        return data

    def test(self):
        print(self.get('https://2ip.ru'))

    def __del__(self):
        try:
            self.playwright.stop()
        except Exception:
            pass
