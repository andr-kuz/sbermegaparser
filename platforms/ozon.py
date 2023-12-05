from platforms.platform import Platform
from entities.products import OzonProduct
from exceptions import OzonTryAgainException
import time

class Ozon(Platform):
    stalled_attempts: int = 0
    stalled_text = 'Доступ ограничен'
    entities_regex = {
        'https://www.ozon.ru/product/[a-zA-Z0-9-]+?/': OzonProduct
    }

    def _is_client_broken(self, page_data: str) -> bool | None:
        if self.stalled_text and self.stalled_text in page_data:
            self.stalled_attempts += 1
            if self.stalled_attempts > 3:
                return True
            time.sleep(5)
            raise OzonTryAgainException
        self.stalled_attempts = 0
