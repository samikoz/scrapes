import datetime
import logging
from typing import Iterator, Dict, List, Tuple

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from camerascrape.types import CameraType
from camerascrape.items import CameraOffer
from camerascrape.parsers.olx import OlxCameraParser


logger = logging.getLogger(__name__)


class OlxSpider(CrawlSpider):
    name = "olx"
    start_urls: Dict[CameraType, str] = {
        CameraType.DSLR: r"https://www.olx.pl/elektronika/fotografia/lustrzanki/?courier=1",
        CameraType.MIRRORLESS: r"https://www.olx.pl/elektronika/fotografia/bezlusterkowce/?courier=1"
    }
    rules = (
        Rule(LinkExtractor(allow='.*/oferta/.*'), callback='parse_camera'),
    )

    def __init__(self, name: str = "olx", typ: CameraType = CameraType.ALL, initial_pages: int = 1, **kwargs) -> None:
        super().__init__(name, **kwargs)
        self._camera_type: CameraType = typ
        self._parser = OlxCameraParser()

        self._initial_pages: int = initial_pages
        self._scrape_time = datetime.datetime.now()

    @property
    def scrape_timestamp(self) -> int:
        return int(self._scrape_time.timestamp())

    def start_requests(self) -> Iterator[scrapy.Request]:
        types_and_pages: List[Tuple[CameraType, int]] = []
        if self._camera_type == CameraType.ALL:
            types_and_pages.extend([(CameraType.DSLR, i) for i in range(1, self._initial_pages + 1)])
            types_and_pages.extend([(CameraType.MIRRORLESS, i) for i in range(1, self._initial_pages + 1)])
        else:
            types_and_pages.extend([(self._camera_type, i) for i in range(1, self._initial_pages + 1)])

        return (scrapy.Request(url=self._format_starting_url(typ, i), callback=self.parse)
                    for typ, i in types_and_pages)

    def _format_starting_url(self, camera_type: CameraType, page_no: int) -> str:
        return f'{self.start_urls.get(camera_type)}&page={page_no}'

    def parse(self, response, **kwargs):
        logger.info(f"parsing {response.url}")
        return self._parse(response, **kwargs)

    def parse_camera(self, response) -> CameraOffer:
        return self._parser.parse(response)
