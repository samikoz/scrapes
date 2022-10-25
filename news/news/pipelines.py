import scrapy

from news.persistors import SqlitePersistor


class PersistencePipeline:
    def __init__(self) -> None:
        self._persistor = SqlitePersistor()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> scrapy.Item:
        self._persistor.connect()
        self._persistor.persist(item, "theguardian")
        self._persistor.close()
        return item
