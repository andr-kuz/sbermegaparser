class ClientBrokenException(Exception):
    def __init__(self):
        self.message = 'Change IP'

    def __str__(self):
        return self.message


class OzonTryAgainException(Exception):
    def __init__(self):
        self.message = """
        Доступ ограничен. Чтобы решить проблему, попробуйте сделать это:
            Отключить VPN, если он используется
            Немного подождать и нажать на кнопку «Обновить»
            Подключиться к другому WI-FI или мобильной сети
            Перезагрузить домашний роутер, если используется домашний WI-FI
        """

    def __str__(self):
        return self.message
