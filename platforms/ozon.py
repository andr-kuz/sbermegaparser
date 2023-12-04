from platforms.platform import Platform
from entities.products import OzonProduct

class Ozon(Platform):
    entities_regex = {
        'https://www.ozon.ru/product/[a-zA-Z0-9-]+?/': OzonProduct
    }
