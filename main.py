import sys
from sber_scraper import SberScraper
from selenium_driver import SeleniumDriver


def main(urls: list):
    driver = SeleniumDriver()
    scraper = SberScraper(driver.driver)
    for url in urls:
        data = scraper.get_product(url.strip())
        print(data)

if __name__ == '__main__':
    if sys.argv[1] == '-f' and sys.argv[2]:
        with open(sys.argv[2]) as file:
            urls = list(file)
            main(urls)
    else:
        main([sys.argv[1]])
