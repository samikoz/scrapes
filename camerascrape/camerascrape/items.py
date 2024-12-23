import scrapy


class CameraItem(scrapy.Item):
    url = scrapy.Field()
    producer = scrapy.Field()
    model = scrapy.Field()
    release = scrapy.Field()
    pixels = scrapy.Field()
    aspect_ratios = scrapy.Field()
    resolution = scrapy.Field()
    matrix_size = scrapy.Field()
    iso_range = scrapy.Field()
    inverse_mechanical_shutter = scrapy.Field()
    inverse_electronic_shutter = scrapy.Field()
    weight = scrapy.Field()
    dimensions = scrapy.Field()
    exceptions = scrapy.Field()


class CameraOffer(scrapy.Item):
    url = scrapy.Field()
    # title = scrapy.Field()
    # created_at = scrapy.Field()
    # description = scrapy.Field()
    # camera = scrapy.Field()
    # source = scrapy.Field()
    # country = scrapy.Field()
