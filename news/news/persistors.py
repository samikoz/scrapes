import hashlib
import sqlite3

from news.items import NewsItem
import news.settings


class SqlitePersistor:
    _sqlite_file: str = news.settings.sqlite_file

    connection = None
    cursor = None

    def connect(self) -> None:
        self.connection = sqlite3.connect(self._sqlite_file)
        self.cursor = self.connection.cursor()

    def persist(self, item: NewsItem, tablename: str) -> None:
        self.cursor.execute(
            f"INSERT INTO {tablename} VALUES (?, ?, ?) ON CONFLICT(title_hash) DO NOTHING",
            (self._hash(item["title"]), item["title"], item["url"])
        )
        self.connection.commit()

    @staticmethod
    def _hash(text: str) -> str:
        return hashlib.sha1(text.encode("utf-8")).hexdigest()

    def close(self) -> None:
        self.connection.close()
