import scrapy


class CameraItem(scrapy.Item):
    # url = scrapy.Field()
    producer = scrapy.Field()
    model = scrapy.Field()
    release = scrapy.Field()
    pixels = scrapy.Field()
    # resolutions = scrapy.Field()
    # matrix_size = scrapy.Field()
    # matrix_type = scrapy.Field()
    # matrix_info = scrapy.Field()
    # iso_range = scrapy.Field()
    # shutter_range = scrapy.Field()
    # video_modes = scrapy.Field()
    # weight = scrapy.Field()
    # dimensions = scrapy.Field()


class CameraOffer(scrapy.Item):
    url = scrapy.Field()
    # title = scrapy.Field()
    # created_at = scrapy.Field()
    # description = scrapy.Field()
    # camera = scrapy.Field()
    # source = scrapy.Field()
    # country = scrapy.Field()
