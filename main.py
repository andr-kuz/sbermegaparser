from sber_scraper import SberScraper
from selenium_driver import SeleniumDriver


driver = SeleniumDriver()
scraper = SberScraper(driver.driver)
makfa = scraper.get_product('https://megamarket.ru/catalog/details/makaronnye-izdeliya-makfa-spirali-450-g-100023361193/')
print(makfa)
