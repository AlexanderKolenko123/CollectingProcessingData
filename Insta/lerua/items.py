# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def clear_price(value):
    try:
        value = int(value.replace('\xa0', ''))
    except:
        pass
    return value

def clear_price_lerua(value):
    try:
        value = int(value.replace(' ', ''))
    except:
        pass
    return value

class AvitoparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(default=None, output_processor=TakeFirst(), input_processor=MapCompose(clear_price_lerua))
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())

class LeruaParcerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(default=None, output_processor=TakeFirst(), input_processor=MapCompose(clear_price))
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())

class InstaParcerItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    follower_id = scrapy.Field()
    following_id = scrapy.Field()
    username = scrapy.Field()
    photo = scrapy.Field()

