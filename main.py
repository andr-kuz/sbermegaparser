from utils import count_process
from selenium_client import SeleniumClient
from selenium_driver import SeleniumDriver
from client import ClientStalledException
import argparse


def main(urls: list, pause: int = 0, proxy: str = ''):
    driver = SeleniumDriver(proxy)
    client = SeleniumClient(driver.driver)
    for url in urls:
        url = url.strip()
        result = {}
        try:
            product = client.get_product(url)
        except ClientStalledException:
            print('stalled')
            break
        result = '{"' + url + '":' + product.as_string() + '}'
        print(result, flush=True)
        driver.driver.implicitly_wait(pause)

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
