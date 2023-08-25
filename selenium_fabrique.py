from fabrique import Fabrique
from selenium_client import SeleniumClient
from selenium_driver import SeleniumDriver

class SeleniumFabrique(Fabrique):
    def _init_client(self, proxy: str) -> SeleniumClient:
        driver = SeleniumDriver(proxy)
        client = SeleniumClient(driver.driver)
        return client
