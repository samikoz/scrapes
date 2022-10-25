from typing import Optional
import hashlib
import sqlite3

from flatscrape.items import FlatOfferItem
import flatscrape.settings


class SqliteItemPersistor:
    _sqlite_file: str = flatscrape.settings.sqlite_file
    _table_name: str = "flats"

    connection = None
    cursor = None

    def connect(self) -> None:
        self.connection = sqlite3.connect(self._sqlite_file)
        self.cursor = self.connection.cursor()

    def persist(self, item: FlatOfferItem) -> None:
        created_at_timestamp: Optional[int] = int(item.get("created_at").timestamp()) if item.get("created_at") else None
        self.cursor.execute(
            f"INSERT INTO {self._table_name} VALUES (?, ?, ?, ?, ?) ON CONFLICT(title_hash) DO NOTHING",
            (self._hash(item["title"]), item["title"], item["url"], created_at_timestamp, item["scrape_timestamp"])
        )
        self.connection.commit()

    @staticmethod
    def _hash(text: str) -> str:
        return hashlib.sha1(text.encode("utf-8")).hexdigest()

    def close(self) -> None:
        self.connection.close()
