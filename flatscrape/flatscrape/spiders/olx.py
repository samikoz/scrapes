import datetime
from typing import Optional, List, Iterator
import logging

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from flatscrape.items import FlatOfferItem
from flatscrape.parsers.olx import OLXFlatOfferParser
from flatscrape.parsers.otodom import OtodomOfferParser


logger = logging.getLogger(__name__)


class OLXSpider(CrawlSpider):
    name = "olx"
    base_url = "https://www.olx.pl/nieruchomosci/mieszkania/"
    rules = (
        Rule(LinkExtractor(allow='.*/oferta/.*'), callback='parse_offer'),
    )

    def __init__(self, name: str = None, city: Optional[str] = None, price_from: Optional[int] = None,
                 price_to: Optional[int] = None, radius: Optional[int] = None, initial_pages: int = 1, **kwargs) -> None:

        super().__init__(name, **kwargs)
        self._city: Optional[str] = city
        self._price_from: Optional[int] = price_from
        self._price_to: Optional[int] = price_to
        self._radius: Optional[int] = radius
        self._initial_pages: Optional[int] = initial_pages

        self._scrape_time = datetime.datetime.now()
        self._olx_parser = OLXFlatOfferParser()
        self._otodom_parser = OtodomOfferParser()

    @property
    def scrape_timestamp(self) -> int:
        return int(self._scrape_time.timestamp())

    def start_requests(self) -> Iterator[scrapy.Request]:
        return (scrapy.Request(url=self._format_starting_url(i), callback=self.parse)
                for i in range(1, self._initial_pages + 1))

    def _format_starting_url(self, page_no: int) -> str:
        specific_url: str = self.base_url
        appendables: List[str] = []

        if self._city:
            specific_url += self._city
        if self._price_from:
            appendables.append(f"search[filter_float_price:from]={self._price_from}")
        if self._price_to:
            appendables.append(f"search[filter_float_price:to]={self._price_to}")
        if self._radius:
            appendables.append(f"search[dist]={self._radius}")
        appendables.append(f"page={page_no}")

        starting_url: str = specific_url + "?" + "&".join(appendables)
        logger.info(f"scraping from {starting_url}")
        return starting_url

    def parse(self, response, **kwargs):
        return self._parse(response, **kwargs)

    def parse_offer(self, response) -> FlatOfferItem:
        """olx contains offers from otodom as well."""

        if 'www.olx.pl' in response.url:
            return self._olx_parser.parse(response)
        if 'www.otodom.pl' in response.url:
            return self._otodom_parser.parse(response)

        logger.info("unrecognised url.")
