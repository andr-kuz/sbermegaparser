from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('--headless')

class SeleniumDriver:
    def __init__(self):
        self.driver = webdriver.Remote("http://firefox:4444/wd/hub", options=options)

    def __repr__(self):
        return self.driver

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
