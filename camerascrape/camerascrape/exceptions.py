class OptyczneParsingException(Exception):
    pass


class OptyczneSubparserException(Exception):
    def __init__(self, parsee: str, exc: Exception) -> None:
        super().__init__(parsee)
        self.parsee: str = parsee
        self.exception = exc
