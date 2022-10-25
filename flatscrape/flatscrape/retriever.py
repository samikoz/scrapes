import sqlite3
from datetime import datetime
from typing import NamedTuple, Optional, List

import flatscrape.settings


class RetrievedOffer(NamedTuple):
    title: str
    url: str
    creation_time: Optional[datetime]


class OfferRetriever:
    connection = None
    cursor = None

    def connect(self) -> None:
        self.connection = sqlite3.connect(flatscrape.settings.sqlite_file)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def get_offers(self, scrape_timestamp: int) -> List[RetrievedOffer]:
        retrieved_rows: List[sqlite3.Row] = list(self.cursor.execute(
            "select * from flats where scrape_time=?;",
            (scrape_timestamp,)
        ))
        return sorted(
            [RetrievedOffer(row["title"], row["url"], self._parse_creation_time(row["creation_time"])) for row in retrieved_rows],
            key=lambda offer: offer.creation_time or datetime.fromtimestamp(1),
            reverse=True
        )

    @staticmethod
    def _parse_creation_time(timestamp: Optional[int]) -> Optional[datetime]:
        return datetime.fromtimestamp(timestamp) if timestamp else None

    def close(self) -> None:
        self.connection.close()
