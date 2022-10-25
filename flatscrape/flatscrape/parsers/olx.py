import re
import requests
import logging
from datetime import datetime
from typing import Optional, Dict

from flatscrape.items import OLXFlatOfferItem
from flatscrape.olx_offer_api import OLXOfferAPIResponse
from flatscrape.exceptions import OLXParsingException


logger = logging.getLogger(__name__)


class OLXFlatOfferParser:
    _api_url: str = "https://www.olx.pl/api/v1/offers/{}"

    def parse(self, response) -> OLXFlatOfferItem:
        offer_id: str = response.xpath("//div[@data-cy='ad-footer-bar-section']/span/text()").getall()[1]

        api_call = requests.get(self._api_url.format(offer_id))
        api_response: OLXOfferAPIResponse = OLXOfferAPIResponse.from_api_call(api_call)

        try:
            item = OLXFlatOfferItem()
            item["id"] = offer_id
            item["url"] = response.url
            item["title"] = api_response.title
            item["created_at"] = datetime.fromisoformat(api_response.created_time)
            item["price"] = self._parse_price(api_response.parameters)
            item["size"] = self._parse_size(api_response.parameters)
            item["rooms_no"] = self._parse_rooms(api_response.parameters)
            item["description"] = api_response.description
            item["city"] = self._parse_city(api_response.location)
        except KeyError as e:
            logger.warning(f"olx offer unexpected structure. {str(e)}. response: {api_response}")
            raise OLXParsingException(api_response)

        return item

    @staticmethod
    def _parse_city(location_data: Dict) -> str:
        return location_data["city"]["name"]

    @staticmethod
    def _parse_price(offer_parameters: Dict) -> Optional[int]:
        base_price: int = offer_parameters["price"]["value"]
        additional_rent: int = int(offer_parameters.get("rent", {"key": 0})["key"])
        return base_price + additional_rent

    @staticmethod
    def _parse_size(offer_parameters: Dict) -> Optional[int]:
        if size := offer_parameters["m"]["key"]:
            return int(re.match(r"\d+", size).group(0))

    @staticmethod
    def _parse_rooms(offer_parameters: Dict) -> Optional[int]:
        rooms_label: str = offer_parameters["rooms"]["label"]
        if rooms_label == "Kawalerka":
            return 1

        if rooms_no := re.match(r"\d", rooms_label):
            return int(rooms_no.group(0))
