from seleniumwire import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from clients.client import Client
from pyvirtualdisplay.display import Display


class Firefox(Client):
    def __init__(self, proxy_address: str):
        self.proxy = proxy_address
        display = Display(visible=False, size=(800, 600))
        display.start()

        options = webdriver.FirefoxOptions()
        options.page_load_strategy = 'eager'
        sw_options = {
            'proxy': {
                'http': self.proxy,
                'https': self.proxy,
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

        self.driver = webdriver.Firefox(options=options, seleniumwire_options=sw_options)
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
