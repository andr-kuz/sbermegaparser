from selenium.webdriver.firefox.webdriver import WebDriver

class Client:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get(self, url: str):
        self.driver.get(url)
        return self.driver.page_source
