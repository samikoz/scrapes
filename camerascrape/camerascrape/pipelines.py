import sqlite3
import itertools
import logging
from typing import List

from camerascrape.items import CameraItem
import camerascrape.settings


logger = logging.getLogger(__name__)


class PersistencePipeline:
    _sqlite_file: str = camerascrape.settings.sqlite_file
    _table_name: str = "cameras"
    _db_columns: List[str] = [
        "producer str NOT NULL",
        "model str NOT NULL",
        "url str NOT NULL",
        "release str",
        "pixels real",
        "resolution_width int",
        "resolution_height int",
        "matrix_width real",
        "matrix_height real",
        "iso_low int",
        "iso_high int",
        "inverse_mechanical_shutter int",
        "inverse_electronic_shutter int",
        "weight real",
        "length real",
        "width real",
        "height real"
    ]
    db_primary_key: str = "PRIMARY KEY (producer, model)"

    connection = None
    cursor = None
    release_date_format: str = "%Y-%m-%d"
    cache_count: int = 100
    items: List[CameraItem] = []

    def open_spider(self, spider):
        self.connection = sqlite3.connect(self._sqlite_file)
        self.cursor = self.connection.cursor()

        create_table_query: str = "create table if not exists cameras(" + ', '.join(self._db_columns) + ', ' + self.db_primary_key + ');'
        self.cursor.execute(create_table_query)

    def close_spider(self, spider):
        if self.items:
            self._persist_items()
        self.connection.close()

    def process_item(self, item: CameraItem, spider) -> CameraItem:
        self.items.append(item)
        if len(self.items) == self.cache_count:
            self._persist_items()
        return item

    def _persist_items(self):
        table_part: str = f"INSERT INTO {self._table_name} "
        values_part: str = "VALUES " + (('(' + ('?,'*len(self._db_columns))[:-1] + '),') * len(self.items))[:-1]
        conflict_part: str = " ON CONFLICT(producer,model) DO NOTHING"

        logger.info(f"persisting {len(self.items)} items")
        self.cursor.execute(
            table_part + values_part + conflict_part,
            list(itertools.chain(*[self._unpack_item(it) for it in self.items]))
        )
        self.connection.commit()
        self.items = []

    def _unpack_item(self, item: CameraItem) -> List:
        release_date: str = item["release"].strftime(self.release_date_format) if item.get("release") else None
        resolution_width, resolution_height = (item["resolution"][0], item["resolution"][1]) if item.get("resolution") else (None, None)
        matrix_width, matrix_height = (item["matrix_size"][0], item["matrix_size"][1]) if item.get("matrix_size") else (None, None)
        iso_low, iso_high = (item["iso_range"][0], item["iso_range"][1]) if item.get("iso_range") else (None, None)
        length, width, height = (item["dimensions"][0], item["dimensions"][1], item["dimensions"][2]) if item.get("dimensions") else (None, None,None)
        return [
            item["producer"],
            item["model"],
            item["url"],
            release_date,
            item.get("pixels"),
            resolution_width,
            resolution_height,
            matrix_width,
            matrix_height,
            iso_low,
            iso_high,
            item["inverse_mechanical_shutter"],
            item["inverse_electronic_shutter"],
            item["weight"],
            length,
            width,
            height
        ]
