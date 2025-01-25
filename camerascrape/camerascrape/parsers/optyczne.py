import logging
from typing import Dict, Any, Tuple, Iterable

from camerascrape.items import CameraItem
from camerascrape.exceptions import OptyczneSubparserException
from camerascrape.parsers.optyczne_table_parsers import (DateParser, PixelsParser, ResolutionParser, MatrixSizeParser,
                                                         ISOParser, ShutterParser, WeightParser, DimensionsParser,
                                                         OptyczneTableParser, VacuousParser)



logger = logging.getLogger(__name__)


class OptyczneCameraParser:
    row_parsers: Dict[str, OptyczneTableParser] = {
        "Producent": VacuousParser('producer'),
        "Model": VacuousParser('model'),
        "Data premiery": DateParser(),
        "Liczba pikseli": PixelsParser(),
        "Dostępne rozdzielczości": ResolutionParser(),
        "Matryca": MatrixSizeParser(),
        "Zakres ISO": ISOParser(),
        "Migawka": ShutterParser(),
        "Waga": WeightParser(),
        "Wymiary": DimensionsParser()
    }

    def parse(self, response) -> CameraItem:
        item = CameraItem()
        item["exceptions"] = []
        for tr in response.xpath("//div[@class='panel-content']/table/tbody/tr"):
            field: str = tr.xpath("./th/text()").get()
            if field in self.row_parsers.keys():
                try:
                    row_to_parse: str = ''.join(tr.xpath("./td/text()").getall())
                    for field_name, parsed_field in self.row_parsers.get(field).parse(row_to_parse):
                        item[field_name] = parsed_field
                except OptyczneSubparserException as e:
                    item["exceptions"].append(e)
                    for field_name in e.parsed_fields:
                        item[field_name] = None


        item["url"] = response.url
        if len(item["exceptions"]) > 0:
            exc_message: str = f"exceptions parsing {response.url}:\n" + '\n'.join(f" {exc.parsed_fields}:{exc.exception}" for exc in item["exceptions"])
            logger.warning(exc_message)
        return item
