import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Iterable, List
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from flatscrape.retriever import OfferRetriever, RetrievedOffer
from furtive import SMTP_SERVER, SMTP_PASSWORD, SMTP_PORT, SENDER_EMAIL, RECIPIENT_EMAIL


logger = logging.getLogger(__name__)


def _render_message(offers: Iterable[RetrievedOffer]) -> str:
    now: datetime = datetime.now()
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Flats {now.month:02d}{now.day:02d}:{now.hour:02d}{now.minute:02d}"
    message["From"] = SENDER_EMAIL
    message["To"] = RECIPIENT_EMAIL
    text: str = "\n".join(f"{offer.title}\n{offer.url}\n{offer.creation_time if offer.creation_time else '-'}\n" for offer in offers)
    message.attach(MIMEText(text, "plain"))
    return message.as_string()


process = CrawlerProcess(get_project_settings())
process.crawl("olx", city="Sopot", price_from=1200, price_to=3000, radius=6, initial_pages=1)
scrape_timestamp: int = process.crawlers.pop().spider.scrape_timestamp
process.start()

retriever: OfferRetriever = OfferRetriever()
retriever.connect()
retrieved_offers: List[RetrievedOffer] = retriever.get_offers(scrape_timestamp)
retriever.close()


if retrieved_offers:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ssl.create_default_context()) as server:
        server.login(SENDER_EMAIL, SMTP_PASSWORD)
        message_body: str = _render_message(retrieved_offers)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message_body)
else:
    logger.info("no offers were found")
