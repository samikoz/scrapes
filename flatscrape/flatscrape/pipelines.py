import re
from scrapy.exceptions import DropItem

from flatscrape.items import FlatOfferItem
from flatscrape.spiders.olx import OLXSpider
from flatscrape.persistors import SqliteItemPersistor


class FilterPipeline:
    accepted_cities: re.Pattern = re.compile(r"(Gda|Sopot|Gdy)")
    # holidays: re.Pattern = re.compile(r"(wakacje|wczasy|września|kr[óo]tkotermin)", re.I)
    shitholes: re.Pattern = re.compile(r"(kokoszk|nowy port|moren|osow|rumi|witomin|dąbrow|matarni|jasie|fikakow|chwarzn)", re.I)

    min_size: int = 30

    min_price: int = 1200
    max_price: int = 3000

    def process_item(self, item: FlatOfferItem, spider) -> FlatOfferItem:
        if not self.min_price <= item['price'] <= self.max_price:
            raise DropItem(f"flat price is out of bounds: {item['price']}")

        if not self.accepted_cities.match(item["city"]):
            raise DropItem(f"flat city unwanted: {item['city']}")

        if not item['size'] >= self.min_size:
            raise DropItem(f"flat size too small: {item['size']}")

        if item['rooms_no'] > 2:
            raise DropItem(f"too many rooms: {item['rooms_no']}")

        # if re.search(self.holidays, item['title']):
        #     raise DropItem(f"only seasonal rent: {item['title']}")

        if re.search(self.shitholes, item['title'] + item['description']):
            raise DropItem(f"faraway district: {item['title']}")

        return item


class PersistencePipeline:
    def __init__(self) -> None:
        self._persistor = SqliteItemPersistor()

    def process_item(self, item: FlatOfferItem, spider: OLXSpider) -> FlatOfferItem:
        item["scrape_timestamp"] = spider.scrape_timestamp
        self._persistor.connect()
        self._persistor.persist(item)
        self._persistor.close()
        return item
