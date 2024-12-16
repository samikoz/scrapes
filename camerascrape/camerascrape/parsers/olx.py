from camerascrape.items import CameraOffer


class OlxCameraParser:
    def parse(self, response) -> CameraOffer:
        item: CameraOffer = CameraOffer()
        item["url"] = response.url
        return item
