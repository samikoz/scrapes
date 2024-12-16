from datetime import datetime
from scrapy.http import HtmlResponse
from betamax import Betamax
from betamax.fixtures.unittest import BetamaxTestCase

from camerascrape.spiders.olx import OlxCameraParser
from camerascrape.items import CameraOffer


with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/responses'
    config.preserve_exact_body_bytes = True


class TestOLXParser(BetamaxTestCase):
    parser = OlxCameraParser()

    def test_olx_parsing(self):
        url: str = "https://www.olx.pl/d/oferta/lustrzanka-canon-eos-4000d-obiektyw-ef-s-18-55mm-f-3-5-5-6-iii-CID99-ID13xGJl.html"
        response = self._prepare_response(url)

        parsed: CameraOffer = self.parser.parse(response)

        assert parsed["url"] == url

    def _prepare_response(self, url: str) -> HtmlResponse:
        response = self.session.get(url)
        scrapy_response = HtmlResponse(body=response.content, url=url)
        return scrapy_response