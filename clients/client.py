from abc import abstractmethod


class Client:
    def __init__(self, proxy_address: str):
        self.proxy = proxy_address

    def __str__(self):
        return f'<{self.__class__.__name__} {self.proxy}>'

    @abstractmethod
    def get(self, url: str, find_css_on_page: str | None = '') -> str:
        pass

    @abstractmethod
    def test(self):
        pass

    @abstractmethod
    def __del__(self):
        pass
