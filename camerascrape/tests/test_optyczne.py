from datetime import date
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

    def test_parsing_sonya1(self):
        url: str = "https://www.optyczne.pl/2427-Sony_A1_II-specyfikacja_aparatu.html"
        response = self._prepare_response(url)

        parsed: CameraItem = self.parser.parse(response)

        assert parsed["url"] == url
        assert parsed["producer"] == "Sony"
        assert parsed["model"] == "A1 II"
        assert parsed["release"] == date(2024,11,19)
        assert abs(parsed["pixels"] - 50.1) < 1e-6
        assert parsed["resolution"] == (8640, 5760)
        assert parsed["matrix_size"] == (35.9, 24.0)
        assert parsed["iso_range"] == (100, 32000)
        assert parsed["inverse_mechanical_shutter"] == 8000
        assert parsed["inverse_electronic_shutter"] == 32000
        assert parsed["weight"] == 743
        assert parsed["dimensions"] == (136.1, 96.9, 82.9)

    def test_parsing_pentaxk3(self):
        url: str = "https://www.optyczne.pl/2390-Pentax_K-3_III_Monochrome-specyfikacja_aparatu.html"
        response = self._prepare_response(url)

        parsed: CameraItem = self.parser.parse(response)

        assert parsed["url"] == url
        assert parsed["producer"] == "Pentax"
        assert parsed["model"] == "K-3 III Monochrome"
        assert parsed["release"] == date(2023,4,13)
        assert abs(parsed["pixels"] - 25.7) < 1e-6
        assert parsed["resolution"] == (6192, 4128)
        assert parsed["matrix_size"] == (23.3, 15.5)
        assert parsed["iso_range"] == (200, 1638400)
        assert parsed["inverse_mechanical_shutter"] is None
        assert parsed["inverse_electronic_shutter"] == 8000
        assert parsed["weight"] == 820
        assert parsed["dimensions"] == (134.5, 103.5, 73.5)

    def test_parsing_panasoniclumix(self):
        url: str = "https://www.optyczne.pl/2428-Panasonic_Lumix_DC-G97-specyfikacja_aparatu.html"
        response = self._prepare_response(url)

        parsed: CameraItem = self.parser.parse(response)

        assert parsed["matrix_size"] == (17.3, 13)

    def test_parsing_sigmafpl(self):
        url: str = "https://www.optyczne.pl/2346-Sigma_fp_L-specyfikacja_aparatu.html"
        response = self._prepare_response(url)

        parsed: CameraItem = self.parser.parse(response)

        assert parsed["resolution"] == (9520, 6328)
        assert parsed["inverse_electronic_shutter"] == 8000

    def test_parsing_canoneos850(self):
        url: str = "https://www.optyczne.pl/2300-Canon_EOS_850D-specyfikacja_aparatu.html"
        response = self._prepare_response(url)

        parsed: CameraItem = self.parser.parse(response)

        assert parsed["resolution"] == (6000, 4000)

    def test_parsing_leicas(self):
        url: str = "https://www.optyczne.pl/2028-Leica_S_(Typ_007)-specyfikacja_aparatu.html"
        response = self._prepare_response(url)

        parsed: CameraItem = self.parser.parse(response)

        assert parsed["resolution"] == (7500, 5000)
        assert parsed["inverse_mechanical_shutter"] == 4000
        assert parsed["inverse_electronic_shutter"] is None

    def test_parsing_nikond5500(self):
        url: str = "https://www.optyczne.pl/1935-Nikon_D5500-specyfikacja_aparatu.html"
        response = self._prepare_response(url)

        parsed: CameraItem = self.parser.parse(response)

        assert parsed["iso_range"] == (100, 25600)

    def _prepare_response(self, url: str) -> HtmlResponse:
        response = self.session.get(url)
        scrapy_response = HtmlResponse(body=response.content, url=url)
        return scrapy_response