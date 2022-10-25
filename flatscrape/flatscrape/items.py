import scrapy


class FlatOfferItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    created_at = scrapy.Field()
    scrape_timestamp = scrapy.Field()
    city = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
    rooms_no = scrapy.Field()
    description = scrapy.Field()


class OLXFlatOfferItem(FlatOfferItem):
    id = scrapy.Field()


class OtodomFlatOfferItem(FlatOfferItem):
    pass
