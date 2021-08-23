# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EbirdItem(scrapy.Item):

    code=scrapy.Field()
    scientific_name=scrapy.Field()
    common_name=scrapy.Field()
    description=scrapy.Field()
    image=scrapy.Field()
    audio=scrapy.Field()
    url=scrapy.Field()