import re
import logging
from typing import List

from flatscrape.items import OtodomFlatOfferItem
from flatscrape.exceptions import OLXParsingException


logger = logging.getLogger(__name__)


class OtodomOfferParser:
    _possible_cities: List[str] = ['Sopot', 'Gdańsk']

    def parse(self, response) -> OtodomFlatOfferItem:
        item = OtodomFlatOfferItem()
        item["url"] = response.url
        item["title"] = response.xpath("//h1[@data-cy='adPageAdTitle']/text()").get()
        item["city"] = self._parse_city(response)
        item["price"] = int(re.sub(r"\D", "", response.xpath("//strong[@data-cy='adPageHeaderPrice']/text()").get()))
        item["size"] = self._parse_otodom_detail(response, "Powierzchnia")
        item["rooms_no"] = self._parse_otodom_detail(response, "Liczba pokoi")
        item["description"] = "".join(response.xpath("//div[@data-cy='adPageAdDescription']//p/text()").getall())
        return item

    def _parse_city(self, response) -> str:
        adres: str = response.xpath("//a[@aria-label='Adres']/text()").get()
        for possible_city in self._possible_cities:
            if possible_city in adres:
                return possible_city

        logger.warning(f"otodom offer unrecognised city. address: {adres}")
        raise OLXParsingException(response.url)

    @staticmethod
    def _parse_otodom_detail(response, title: str) -> int:
        if match := re.match(r"\d+", response.xpath(f"//div[@aria-label='{title}']/child::div/child::div/text()").getall()[-1]):
            return int(match.group(0))
        logger.warning(f"otodom offer unexpected structure. detail-'{title}' parsing. {response.url}")
        raise OLXParsingException(response.url)
