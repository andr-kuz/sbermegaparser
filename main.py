from utils import count_process
from factory import Factory
from selenium_client import SeleniumClient
import argparse


def main(urls: list, proxies: list, pause: int = 0):
    factory = Factory(proxies, SeleniumClient)
    for url in urls:
        url = url.strip()
        result = {}
        product = factory.run(SeleniumClient.get_product, url)
        result = '{"' + url + '":' + product.asas() + '}'
        print(result, flush=True)
        factory.run(SeleniumClient.sleep, pause)

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
