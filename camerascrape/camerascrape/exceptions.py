class OptyczneParsingException(Exception):
    pass


class OptyczneSubparserException(Exception):
    def __init__(self, parsee: str) -> None:
        super(parsee)
        self.parsee: str = parsee
