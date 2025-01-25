from typing import List


class OptyczneParsingException(Exception):
    pass


class OptyczneSubparserException(Exception):

    def __init__(self, parsed_fields: List[str], exc: Exception) -> None:
        super().__init__(parsed_fields)
        self.parsed_fields: List[str] = parsed_fields
        self.exception = exc
