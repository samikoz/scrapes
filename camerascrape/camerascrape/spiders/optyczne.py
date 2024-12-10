import datetime
import logging
from typing import Iterator

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from camerascrape.types import CameraType
from camerascrape.items import CameraItem
from camerascrape.parsers.camera import OptyczneCameraParser


logger = logging.getLogger(__name__)


class OptyczneSpider(CrawlSpider):
    name = "optyczne"
    base_url = r"https://www.optyczne.pl/index.html"
    rules = (
        Rule(LinkExtractor(allow='.*specyfikacja_aparatu\\.html$'), callback='parse_camera'),
    )

    def __init__(self, name: str = "optyczne", typ: CameraType = CameraType.ALL, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self._camera_type: CameraType = typ
        self._parser = OptyczneCameraParser()

        self._scrape_time = datetime.datetime.now()

    @property
    def scrape_timestamp(self) -> int:
        return int(self._scrape_time.timestamp())

    def start_requests(self) -> Iterator[scrapy.Request]:
        if self._camera_type == CameraType.ALL:
            return (scrapy.Request(url=self._format_starting_url(typ), callback=self.parse)
                    for typ in (CameraType.DSLR, CameraType.MIRRORLESS))
        else:
            return (scrapy.Request(url=self._format_starting_url(typ), callback=self.parse)
                    for typ in (self._camera_type,))

    def _format_starting_url(self, camera_type: CameraType) -> str:
        search_params_template: str = r"?aparat=all&producent=&aparat=all&pix=0&zoom=0&typ={}&szukaj=Wyszukaj&sort="

        return f"{self.base_url}{search_params_template.format(camera_type.value)}"

    def parse(self, response, **kwargs):
        logger.info(f"parsing {response.url}")
        return self._parse(response, **kwargs)

    def parse_camera(self, response) -> CameraItem:
        return self._parser.parse(response)
