import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


logger = logging.getLogger(__name__)


process = CrawlerProcess(get_project_settings())
process.crawl("theguardian")
process.start()
