from utils import count_process
from facade import Facade
import argparse
from selenium.common.exceptions import TimeoutException
from platform_factory import PlatformFactory

RETRY_EXCEPTIONS = (TimeoutException)


def main(urls: list, proxies: list, pause: int = 0):
    platform = PlatformFactory.detect_platform(urls[0])
    platform = platform(pause)
    facade = Facade(platform, proxies, 10)
    max_exceptions = 3
    exceptions_counter = 0
    for url in urls:
        url = url.strip()
        result = {}
        while True:
            try:
                product = facade.get(url)
                exceptions_counter = 0
                result = '{"' + url + '":' + product.as_json() + '}'
                print(result, flush=True)
                break
            except RETRY_EXCEPTIONS:
                exceptions_counter += 1
                if exceptions_counter == max_exceptions:
                    break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Scrape data from several marketplaces'
    )
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
