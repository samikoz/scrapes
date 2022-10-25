from datetime import datetime
from scrapy.http import HtmlResponse
from betamax import Betamax
from betamax.fixtures.unittest import BetamaxTestCase

from flatscrape.parsers.otodom import OtodomOfferParser
from flatscrape.items import OtodomFlatOfferItem


with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/responses'
    config.preserve_exact_body_bytes = True


class TestOtodomParser(BetamaxTestCase):
    parser = OtodomOfferParser()

    # fails for current city selection
    # def test_bielany_offer(self):
    #     url: str = "https://www.otodom.pl/pl/oferta/mieszkanie-3-pokoje-57m2-kochanowskiego-bielany-ID4gyls.html"
    #     response = self._prepare_response(url)
    #
    #     parsed: OtodomFlatOfferItem = self.parser.parse(response)
    #
    #     assert parsed["url"] == url
    #     assert parsed["title"] == "Mieszkanie 3 pokoje, 57m2, Kochanowskiego, Bielany"
    #     assert parsed["price"] == 2700
    #     assert parsed["size"] == 57
    #     assert parsed["rooms_no"] == 3
    #     assert parsed["description"].startswith("Do wynajęcie") and parsed["description"].endswith("790022244")
    #     assert parsed["city"] == "Warszawa"

    def _prepare_response(self, url: str) -> HtmlResponse:
        response = self.session.get(url)
        scrapy_response = HtmlResponse(body=response.content, url=url)
        return scrapy_response

