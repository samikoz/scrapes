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

        assert parsed["url"] == url
        assert parsed["producer"] == "Sony"
        assert parsed["model"] == "A1 II"
        assert parsed["release"] == "2024-11-19"
        assert abs(parsed["pixels"] - 50.1) < 1e-6
        assert parsed["aspect_ratios"] == ["[3:2]", "[4:3]", "[16:9]", "[1:1]"]
        assert parsed["resolutions"] == [(8640, 5760), (7680, 5760), (8760, 4864), (5760, 5760)]
        assert parsed["matrix_size"] == (35.9, 24.0)
        assert parsed["iso_range"] == (100, 32000)
        assert parsed["inverse_mechanical_shutter"] == 8000
        assert parsed["inverse_electronic_shutter"] == 32000
        assert parsed["video_modes"] == [(7680, 4320, 30), (3840, 2160, 120), (1920, 1080, 120)]
        assert parsed["weight"] == 743
        assert parsed["dimensions"] == (136.1, 96.9, 82.9)

    def _prepare_response(self, url: str) -> HtmlResponse:
        response = self.session.get(url)
        scrapy_response = HtmlResponse(body=response.content, url=url)
        return scrapy_response