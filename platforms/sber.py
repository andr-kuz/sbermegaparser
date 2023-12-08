from entities.products import SberProduct
from platforms.platform import Platform
from clients.selenium import Selenium

class Sber(Platform):
    stalled_text = 'Запросы с вашего устройства похожи на автоматические'
    entities_regex = {
        'https://megamarket.ru/catalog/details/[a-zA-Z0-9-]+/?$': SberProduct
    }
    client_class = Selenium
    rest_time = 5
