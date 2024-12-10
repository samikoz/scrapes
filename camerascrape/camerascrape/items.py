import scrapy


class CameraItem(scrapy.Item):
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
