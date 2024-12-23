import logging
from typing import Callable, Dict, Any, List

from camerascrape.items import CameraItem
from camerascrape.exceptions import OptyczneSubparserException, OptyczneParsingException
from camerascrape.parsers.optyczne_table_parsers import (date_parser, pixels_parser,
                                                         parse_resolution, parse_matrix_size, parse_iso,
                                                         parse_mechanical_shutter, parse_electronic_shutter,
                                                         parse_weight, parse_dimensions)


logger = logging.getLogger(__name__)


class RowParser:
    def __init__(self, name: str, parser: Callable[[str], Any] = lambda s: s):
        self.field_name: str = name
        self.parser: Callable[[str], Any] = parser


class OptyczneCameraParser:
    row_parsers: Dict[str, List[RowParser]] = {
        "Producent": [RowParser("producer")],
        "Model": [RowParser("model")],
        "Data premiery": [RowParser("release", date_parser)],
        "Liczba pikseli": [RowParser("pixels", pixels_parser)],
        "Dostępne rozdzielczości": [
            RowParser("resolution", parse_resolution)
        ],
        "Matryca": [RowParser("matrix_size", parse_matrix_size)],
        "Zakres ISO": [RowParser("iso_range", parse_iso)],
        "Migawka": [
            RowParser("inverse_mechanical_shutter", parse_mechanical_shutter),
            RowParser("inverse_electronic_shutter", parse_electronic_shutter)
        ],
        "Waga": [RowParser('weight', parse_weight)],
        "Wymiary": [RowParser('dimensions', parse_dimensions)]
    }

    def parse(self, response) -> CameraItem:
        item = CameraItem()
        item["exceptions"] = []
        for tr in response.xpath("//div[@class='panel-content']/table/tbody/tr"):
            field: str = tr.xpath("./th/text()").get()
            if field in self.row_parsers.keys():
                row_parsers: List[RowParser] = self.row_parsers.get(field)
                for parser in row_parsers:
                    try:
                        item[parser.field_name] = parser.parser(''.join(tr.xpath("./td/text()").getall()))
                    except OptyczneSubparserException as e:
                        item[parser.field_name] = None
                        item["exceptions"].append(e)

        item["url"] = response.url
        if len(item["exceptions"]) > 0:
            exc_message: str = f"exceptions parsing {response.url}:\n" + '\n'.join(f" {exc.parsee}:{exc.exception}" for exc in item["exceptions"])
            logger.warning(exc_message)
            # raise OptyczneParsingException(response.url)
        return item
