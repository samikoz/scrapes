from camerascrape.items import CameraItem
from camerascrape.spiders.optyczne import OptyczneSpider
from camerascrape.persistors import SqliteCameraPersistor


class PersistencePipeline:
    def __init__(self) -> None:
        self._persistor = SqliteCameraPersistor()

    def process_item(self, item: CameraItem, spider: OptyczneSpider) -> CameraItem:
        item["scrape_timestamp"] = spider.scrape_timestamp
        self._persistor.connect()
        self._persistor.persist(item)
        self._persistor.close()
        return item
