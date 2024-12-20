import logging
from typing import Callable, Dict, Any, List

from camerascrape.items import CameraItem
from camerascrape.exceptions import OptyczneSubparserException, OptyczneParsingException
from camerascrape.parsers.optyczne_table_parsers import (pixels_parser, parse_aspect_ratios, parse_resolution, parse_matrix_size,
                                                         parse_iso, parse_mechanical_shutter, parse_electronic_shutter,
                                                         parse_video_modes, parse_weight, parse_dimensions)


logger = logging.getLogger(__name__)


class RowParser:
    def __init__(self, name: str, parser: Callable[[str], Any] = lambda s: s):
        self.field_name: str = name
        self.parser: Callable[[str], Any] = parser


class OptyczneCameraParser:
    row_parsers: Dict[str, List[RowParser]] = {
        "Producent": [RowParser("producer")],
        "Model": [RowParser("model")],
        "Data premiery": [RowParser("release")],
        "Liczba pikseli": [RowParser("pixels", pixels_parser)],
        "Dostępne rozdzielczości": [
            RowParser("aspect_ratios", parse_aspect_ratios),
            RowParser("resolutions", parse_resolution)
        ],
        "Matryca": [RowParser("matrix_size", parse_matrix_size)],
        "Zakres ISO": [RowParser("iso_range", parse_iso)],
        "Migawka": [
            RowParser("inverse_mechanical_shutter", parse_mechanical_shutter),
            RowParser("inverse_electronic_shutter", parse_electronic_shutter)
        ],
        "Zapis wideo": [RowParser("video_modes", parse_video_modes)],
        "Waga": [RowParser('weight', parse_weight)],
        "Wymiary": [RowParser('dimensions', parse_dimensions)]
    }

    def __init__(self) -> None:
        self._parsing_exceptions: List[OptyczneSubparserException] = []

    def parse(self, response) -> CameraItem:
        item = CameraItem()
        for tr in response.xpath("//div[@class='panel-content']/table/tbody/tr"):
            field: str = tr.xpath("./th/text()").get()
            if field in self.row_parsers.keys():
                row_parsers: List[RowParser] = self.row_parsers.get(field)
                for parser in row_parsers:
                    try:
                        item[parser.field_name] = parser.parser(''.join(tr.xpath("./td/text()").getall()))
                    except OptyczneSubparserException as e:
                        self._parsing_exceptions.append(e)

        item["url"] = response.url
        if len(self._parsing_exceptions) > 0:
            logger.warning(f'exceptions parsing {response.url}:', ', '.join(exc.parsee for exc in self._parsing_exceptions))
            raise OptyczneParsingException(response.url)
        return item
