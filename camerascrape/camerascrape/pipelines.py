import sqlite3
import itertools
from typing import Optional, List, Any

from camerascrape.items import CameraItem
import camerascrape.settings


class PersistencePipeline:
    _sqlite_file: str = camerascrape.settings.sqlite_file
    _table_name: str = "cameras"

    connection = None
    cursor = None
    column_count: int = 15
    cache_count: int = 100
    items: List[CameraItem] = []

    def open_spider(self, spider):
        self.connection = sqlite3.connect(self._sqlite_file)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
                create table if not exists cameras(
                    producer str NOT NULL, 
                    model str NOT NULL, 
                    url str NOT NULL, 
                    release int, 
                    pixels real, 
                    aspect_ratios str, 
                    resolution_width int,
                    resolution_height int, 
                    matrix_width real,
                    matrix_height real, 
                    iso_low int,
                    iso_high int, 
                    inverse_mechanical_shutter int, 
                    inverse_electronic_shutter int, 
                    weight real, 
                    dimensions str, 
                    PRIMARY KEY (producer, model));
                """)

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
        table_part: str = "INSERT INTO {self._table_name} "
        values_part: str = "VALUES " + (('(' + ('?,'*self.column_count[:-1]) + '),') * len(self.items))[:-1]
        conflict_part: str = " ON CONFLICT(producer,model) DO NOTHING"

        self.cursor.execute(
            table_part + values_part + conflict_part,
            list(itertools.chain(*[self._unpack_item(it) for it in self.items]))
        )
        self.connection.commit()
        self.items = []

    @staticmethod
    def _unpack_item(item: CameraItem) -> List:
        release_timestamp: Optional[int] =  int(item["release"].timestamp()) if item.get("release") else None
        return [
            item["producer"],
            item["model"],
            item["url"],
            release_timestamp,
            item.get("pixels"),
            item.get("resolution")[0],
            item.get("resolution")[1],
            item["matrix_size"][0],
            item["matrix_size"][1],
            item["iso_range"][0],
            item["iso_range"][1],
            item["inverse_mechanical_shutter"],
            item["inverse_electronic_shutter"],
            item["video_modes"],
            item["weight"],
            item["dimensions"]]
