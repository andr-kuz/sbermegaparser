from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Client:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get(self, url: str):
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.header-logo'))).text
        except TimeoutException:
            pass
        return self.driver.page_source
