from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
import os

class Client:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get(self, url: str) -> str:
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.header-logo'))).text
        except TimeoutException:
            return ''
        html = self.driver.page_source
        name = quote(url, '')[-100:]
        path = os.path.abspath(os.path.dirname(__file__))
        with open(path + os.sep + 'temp' + os.sep + name + '.html', 'w') as f:
            f.write(html)
        return self.driver.page_source
