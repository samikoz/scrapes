from datetime import datetime
from scrapy.http import HtmlResponse
from betamax import Betamax
from betamax.fixtures.unittest import BetamaxTestCase

from flatscrape.parsers.olx import OLXFlatOfferParser
from flatscrape.items import OLXFlatOfferItem


with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/responses'
    config.preserve_exact_body_bytes = True


class TestOLXParser(BetamaxTestCase):
    parser = OLXFlatOfferParser()

    def test_elk_offer(self):
        url: str = "https://www.olx.pl/d/oferta/mieszkanie-3-pokoje-40m2-nowe-kolbego-1-meble-widok-jezioro-i-miasto-CID3-IDL77Cp.html#6d46827842"
        response = self._prepare_response(url)

        parsed: OLXFlatOfferItem = self.parser.parse(response)

        assert parsed["id"] == "696185377"
        assert parsed["url"] == url
        assert parsed["title"] == "Mieszkanie 3 pokoje-40m2/Nowe/Kolbego 1/Meble/Widok jezioro i miasto"
        assert parsed["created_at"] == datetime.fromisoformat("2022-05-10T08:04:23+02:00")
        assert parsed["price"] == 2001
        assert parsed["size"] == 29
        assert parsed["rooms_no"] == 3
        assert parsed["description"].startswith("Witam.") and parsed["description"].endswith("Polecam.")
        assert parsed["city"] == "Ełk"

    def test_combined_price(self):
        url: str = "https://www.olx.pl/d/oferta/wynajme-mieszkanie-siedlce-50m2-CID3-IDP8rIK.html"
        response = self._prepare_response(url)

        parsed: OLXFlatOfferItem = self.parser.parse(response)

        assert parsed["price"] == 3150

    def _prepare_response(self, url: str) -> HtmlResponse:
        response = self.session.get(url)
        scrapy_response = HtmlResponse(body=response.content, url=url)
        return scrapy_response

