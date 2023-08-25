from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from client import Client


class SeleniumClient(Client):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def _get_data(self, url: str) -> str:
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.header-logo')))
        except TimeoutException:
            pass
        return self.driver.page_source
