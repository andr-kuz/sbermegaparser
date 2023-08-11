import sys
from sber_scraper import SberScraper
from selenium_driver import SeleniumDriver
import json


def main(urls: list):
    driver = SeleniumDriver()
    scraper = SberScraper(driver.driver)
    result = '{'
    for url in urls:
        if data := scraper.get_product(url.strip()):
           result += '"' + url.strip() + '":' + json.dumps(str(data)) + ','
    result = result[:-1] + '}'
    print(result)

if __name__ == '__main__':
    if sys.argv[1] == '-f' and sys.argv[2]:
        with open(sys.argv[2]) as file:
            urls = list(file)
            main(urls)
    else:
        main([sys.argv[1]])
