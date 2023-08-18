from seleniumwire import webdriver

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')


class SeleniumDriver:
    def __init__(self, proxy_address = ''):
        sw_options = {
            'auto_config': False,
            'addr': 'sberparser',
            'port': 8087,
        }
        proxy = webdriver.Proxy()
        proxy.http_proxy = 'sberparser:8087'
        proxy.ssl_proxy = 'sberparser:8087'
        options.proxy = proxy
        if proxy_address:
            sw_options['proxy'] = {
                'http': proxy_address,
                'https': proxy_address,
            }
        self.driver = webdriver.Remote("http://firefox:4444/wd/hub", options=options, seleniumwire_options=sw_options)
        # debug ip
        # from selenium.webdriver.common.by import By
        # self.driver.get('https://2ip.ru')
        # print(self.driver.find_element(By.CSS_SELECTOR, '#d_clip_button').text)

    def __repr__(self):
        return self.driver

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
