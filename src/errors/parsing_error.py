class ParsingError(Exception):
    """Ошибка парсинга"""
    def __init__(self, message):
        super().__init__(message)
