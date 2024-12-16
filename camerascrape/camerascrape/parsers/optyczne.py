import re
import logging
from typing import Callable, Dict, Any

from camerascrape.items import CameraItem


logger = logging.getLogger(__name__)


class RowParser:
    def __init__(self, name: str, parser: Callable[[str], Any] = lambda s: s):
        self.field_name: str = name
        self.parser: Callable[[str], Any] = parser


class OptyczneCameraParser:
    row_parsers: Dict[str, RowParser] = {
        "Producent": RowParser("producer"),
        "Model": RowParser("model"),
        "Data premiery": RowParser("release"),
        "Liczba pikseli": RowParser("pixels", lambda s: float(s[:-5])),
    }

    def parse(self, response) -> CameraItem:
        item = CameraItem()
        for tr in response.xpath("//div[@class='panel-content']/table/tbody/tr"):
            field: str = tr.xpath("./th/text()").get()
            if field in self.row_parsers.keys():
                row_parser: RowParser = self.row_parsers.get(field)
                item[row_parser.field_name] = row_parser.parser(tr.xpath("./td/text()").get())

        return item
