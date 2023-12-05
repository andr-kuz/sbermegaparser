from utils import count_process
from facade import Facade
from clients.pyppeteer import Pyppeteer
import argparse
from functools import partial
from playwright._impl._errors import TimeoutError
from selenium.common.exceptions import TimeoutException

RETRY_EXCEPTIONS = (TimeoutError, TimeoutException)


def main(urls: list, proxies: list, pause: int = 0):
    platform = Facade.detect_platform_by_url(urls[0])
    platform = platform(pause)
    clients = [partial(Pyppeteer, p) for p in proxies]
    facade = Facade(platform, clients, 120)
    for url in urls:
        url = url.strip()
        result = {}
        count_exceptions = 0
        while True:
            try:
                product = facade.get(url)
                result = '{"' + url + '":' + product.as_json() + '}'
                print(result, flush=True)
                break
            except RETRY_EXCEPTIONS:
                count_exceptions += 1
                if count_exceptions > 3:
                    break

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
        help='provide pause time between urls (default: 0)'
    )
    parser.add_argument(
        '--proxies',
        type=str,
        default='',
        help='provide path to file with proxies list'
    )
    args = parser.parse_args()
    pause = args.p
    urls = []
    if args.f:
        with open(args.f) as file:
            urls = list(file)
    proxies = []
    if args.proxies:
        with open(args.proxies) as file:
            proxies = list(file)
    if count_process(__file__) == 1:
        main(urls, proxies, args.p)
