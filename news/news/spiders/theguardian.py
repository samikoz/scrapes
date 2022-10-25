import logging
from typing import Iterable

import scrapy
from news.items import NewsItem
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor


logger = logging.getLogger(__name__)


class TheGuardianSpider(CrawlSpider):
    name = "theguardian"
    extractor = LinkExtractor(allow="https://www.theguardian.com/.*")

    def start_requests(self) -> Iterable[scrapy.Request]:
        yield scrapy.Request(url="https://www.theguardian.com/international", callback=self.parse)

    def parse(self, response, **kwargs) -> Iterable[NewsItem]:
        return (self._parse_link(link) for link in self.extractor.extract_links(response))

    @staticmethod
    def _parse_link(link) -> NewsItem:
        return NewsItem(title=link.text, url=link.url, source="The Guardian")
