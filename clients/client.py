from abc import abstractmethod

class Client:
    def __init__(self, proxy_address: str):
        self.proxy = proxy_address

    @abstractmethod
    def get(self, url: str, find_css_on_page: str | None = None) -> str:
        pass

    @abstractmethod
    def test(self):
        pass

    @abstractmethod
    def destroy(self):
        pass

    def __del__(self):
        self.destroy()
