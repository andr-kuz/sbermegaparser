from seleniumwire import webdriver

class SeleniumDriver:
    def __init__(self, driver = 'firefox', proxy_address = ''):
        if driver == 'firefox':
            self.driver = self.init_firefox(proxy_address)
        else:
            self.driver = self.init_chrome(proxy_address)
        # debug ip
        # from selenium.webdriver.common.by import By
        # self.driver.get('https://2ip.ru')
        # print(self.driver.find_element(By.CSS_SELECTOR, '#d_clip_button').text)

    def init_firefox(self, proxy_address: str):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
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
        return webdriver.Remote("http://firefox:4444/wd/hub", options=options, seleniumwire_options=sw_options)

    def init_chrome(self, proxy_address: str):
        options = webdriver.ChromeOptions()
        sw_options = {
            'auto_config': False,
            'addr': 'sberparser',
            'port': 8087,
        }
        if proxy_address:
            sw_options['proxy'] = {
                'http': proxy_address,
                'https': proxy_address,
            }
        options.add_argument("enable-automation")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,768")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-gpu")
        options.add_argument("--proxy-server=sberparser:8087")
        return webdriver.Remote("http://chrome:4444/wd/hub", options=options, seleniumwire_options=sw_options)

    def __repr__(self):
        return self.driver

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
