import re
import logging
from typing import Optional, Dict, List

from camerascrape.items import CameraItem


logger = logging.getLogger(__name__)


class OptyczneCameraParser:
    table_to_item_fields: Dict[str, str] = {
        "Producent": "producer",
        "Model": "model",
        "Data premiery": "release",
        "Liczba pixeli": "pixels",
    }

    def parse(self, response) -> CameraItem:
        item = CameraItem()
        for tr in response.xpath("//div[@class='panel-content']/table/tbody/tr"):
            field: str = tr.xpath("./th/text()").get()
            if field in self.table_to_item_fields.keys():
                item[self.table_to_item_fields[field]] = tr.xpath("./td/text()").get()

        return item
