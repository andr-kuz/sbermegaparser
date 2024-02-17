class ClientBrokenException(Exception):
    def __init__(self):
        self.message = 'Change IP'

    def __str__(self):
        return self.message
