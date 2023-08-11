import sys
from sber_scraper import SberScraper
from selenium_driver import SeleniumDriver
import json


def main(urls: list, pause: int | str = 0):
    driver = SeleniumDriver()
    scraper = SberScraper(driver.driver)
    result = '{'
    for url in urls:
        url = url.strip()
        if data := scraper.get_product(url):
           result += '"' + url + '":' + json.dumps(str(data)) + ','
           driver.driver.implicitly_wait(pause)
    result = result[:-1] + '}'
    print(result)

if __name__ == '__main__':
    pause = 0
    if sys.argv[3] == '-p' and sys.argv[4]:
        pause = sys.argv[4]
    if sys.argv[1] == '-f' and sys.argv[2]:
        with open(sys.argv[2]) as file:
            urls = list(file)
            main(urls, pause)
    else:
        main([sys.argv[1]])
