from datetime import datetime


sqlite_file = 'db/camerascrape.db'
BOT_NAME = 'camerascrape'

CURRENT_TIME: datetime = datetime.now()
LOG_FILE = f'logs/{CURRENT_TIME.month:02d}{CURRENT_TIME.day:02d}:{CURRENT_TIME.hour:02d}{CURRENT_TIME.minute:02d}.log'
LOG_LEVEL = 'INFO'

SPIDER_MODULES = ['camerascrape.spiders']
NEWSPIDER_MODULE = 'camerascrape.spiders'

ROBOTSTXT_OBEY = False

# CONCURRENT_REQUESTS = 32

# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# COOKIES_ENABLED = False

# TELNETCONSOLE_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
  'Accept-Encoding': 'gzip, deflate, br',
  'Upgrade-Insecure-Requests': 1,
  'Cache-Control': 'max-age=0',
  'TE': 'Trailers',
}


# SPIDER_MIDDLEWARES = {
#    'camerascrape.middlewares.CamerascrapeSpiderMiddleware': 543,
# }

# DOWNLOADER_MIDDLEWARES = {
#    'camerascrape.middlewares.CamerascrapeDownloaderMiddleware': 543,
# }

# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

ITEM_PIPELINES = {
    'camerascrape.pipelines.PersistencePipeline': 400
}

# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 5
# AUTOTHROTTLE_MAX_DELAY = 60
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# AUTOTHROTTLE_DEBUG = False

# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
