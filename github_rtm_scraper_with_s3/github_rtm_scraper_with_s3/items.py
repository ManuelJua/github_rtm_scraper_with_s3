# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import Identity, TakeFirst, MapCompose,Join


class GithubRtmScraperWithS3Item(scrapy.Item):
    # define the fields for your item here like:
    price=scrapy.Field()
    address=scrapy.Field()
    letting_details=scrapy.Field()
    partial_agent_url=scrapy.Field()
    property_details=scrapy.Field()
    other_features=scrapy.Field()
    description=scrapy.Field()
    date=scrapy.Field()
    
