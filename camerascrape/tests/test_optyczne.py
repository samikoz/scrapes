from datetime import datetime
from scrapy.http import HtmlResponse
from betamax import Betamax
from betamax.fixtures.unittest import BetamaxTestCase

from camerascrape.spiders.optyczne import OptyczneCameraParser
from camerascrape.items import CameraItem


with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/responses'
    config.preserve_exact_body_bytes = True


class TestOptyczneParser(BetamaxTestCase):
    parser = OptyczneCameraParser()

    def test_optyczne_parsing(self):
        url: str = "https://www.optyczne.pl/2427-Sony_A1_II-specyfikacja_aparatu.html"
        response = self._prepare_response(url)

        parsed: CameraItem = self.parser.parse(response)

        # assert parsed["url"] == url
        assert parsed["producer"] == "Sony"
        assert parsed["model"] == "A1 II"
        assert parsed["release"] == "2024-11-19"
        assert abs(parsed["pixels"] - 50.1) < 1e-6
        # assert parsed["resolutions"] == 2001
        # assert parsed["matrix_size"] == 29
        # assert parsed["matrix_type"] == 3
        # assert parsed["iso_range"]
        # assert parsed["shutter_range"]
        # assert parsed["bideo_modes"]
        # assert parsed["weight"]
        # assert parsed["dimensions"]

    def _prepare_response(self, url: str) -> HtmlResponse:
        response = self.session.get(url)
        scrapy_response = HtmlResponse(body=response.content, url=url)
        return scrapy_response