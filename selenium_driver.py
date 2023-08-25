from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import sys

class SeleniumDriver:
    def __init__(self, proxy_address = '', test = False):
        self.driver = self.init_driver(proxy_address)
        if test:
            self.driver.get('https://2ip.ru')
            print('IP:', self.driver.find_element(By.CSS_SELECTOR, '#d_clip_button').text)
            self.driver.get('https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html')
            print('')
            print(self.driver.page_source)
            sys.exit()

    def init_driver(self, proxy_address: str):
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

        driver = webdriver.Remote("http://firefox:4444/wd/hub", options=options, seleniumwire_options=sw_options, desired_capabilities=caps)
        driver.set_page_load_timeout(30)

        return driver

    def __repr__(self):
        return self.driver

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
