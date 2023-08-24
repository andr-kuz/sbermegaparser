from utils import count_process
from sber_scraper import SberScraper
from selenium_driver import SeleniumDriver
import json
import argparse


def main(urls: list, pause: int = 0, proxy: str = ''):
    driver = SeleniumDriver(proxy)
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
    parser = argparse.ArgumentParser(description='Scrape data from sbermegamarket products')
    parser.add_argument(
        '-f',
        type=str,
        help='provide path to file with SberMegaMarket product urls'
    )
    parser.add_argument(
        '-p',
        type=int,
        default=0,
        help='provide pause time between urls (default: 5)'
    )
    parser.add_argument(
        '--proxy',
        type=str,
        default='',
        help='provide proxy (like: socks5://username:password@host:port)'
    )
    args = parser.parse_args()
    pause = args.p
    urls = []
    if args.f:
        with open(args.f) as file:
            urls = list(file)
    if count_process(__file__) == 1:
        main(urls, args.p, args.proxy)
