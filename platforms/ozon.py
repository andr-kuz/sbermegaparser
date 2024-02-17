from platforms.platform import Platform
from entities import OzonProduct
from clients import Firefox


class Ozon(Platform):
    stalled_attempts: int = 0
    stalled_text = 'Checking if the site connection is secure'
    entities_regex = {
        'https://www.ozon.ru/product/[a-zA-Z0-9-]+?/': OzonProduct
    }
    client_class = Firefox
    rest_time = 8

    def _is_client_broken(self, page_data: str) -> bool | None:
        if self.stalled_text and self.stalled_text in page_data:
            return True
