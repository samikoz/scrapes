from __future__ import annotations
from typing import Dict
from attrs import define
import logging

from flatscrape.exceptions import OLXParsingException


logger = logging.getLogger(__name__)


@define
class OLXOfferAPIResponse:
    parameters: Dict
    title: str
    created_time: str
    description: str
    location: Dict

    @classmethod
    def from_api_call(cls, api_response) -> OLXOfferAPIResponse:
        assert api_response.status_code == 200
        try:
            api_response: Dict = api_response.json()["data"]
            parsed_response_params = {item["key"]: item["value"] for item in api_response["params"]}
            return cls(
                parameters=parsed_response_params,
                title=api_response["title"],
                created_time=api_response["last_refresh_time"],
                description=api_response["description"],
                location=api_response["location"]
            )
        except KeyError as e:
            logger.warning(f"olx offer api response unexpected structure. {str(e)}. response: {api_response}")
            raise OLXParsingException(api_response)
