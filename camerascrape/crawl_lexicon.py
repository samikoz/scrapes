import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from camerascrape.types import CameraType


logger = logging.getLogger(__name__)


process = CrawlerProcess(get_project_settings())
process.crawl("optyczne", typ=CameraType.ALL)
process.start()
