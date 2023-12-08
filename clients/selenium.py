from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from clients.client import Client


class Selenium(Client):
    def __init__(self, proxy_address: str):
        self.proxy = proxy_address
        caps = webdriver.DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "eager"

        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        sw_options = {
            'auto_config': False,
            'addr': 'sberparser',
            'port': 8087,
            'proxy': {
                'http': proxy_address,
                'https': proxy_address,
            }
        }

        proxy = webdriver.Proxy()
        proxy.http_proxy = 'sberparser:8087'
        proxy.ssl_proxy = 'sberparser:8087'
        options.proxy = proxy

        self.driver = webdriver.Remote("http://firefox:4444/wd/hub", options=options, seleniumwire_options=sw_options, desired_capabilities=caps)
        self.driver.set_page_load_timeout(30)

    def get(self, url: str, find_css_on_page: str | None = '') -> str:
        self.driver.get(url)
        if find_css_on_page:
            try:
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, find_css_on_page)))
            except TimeoutException:
                pass
        return self.driver.page_source

    def test(self):
        self.driver.get('https://2ip.ru')
        print('IP:', self.driver.find_element(By.CSS_SELECTOR, '#d_clip_button').text)
        self.driver.get('https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html')
        print('')
        print(self.driver.page_source)

    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass
