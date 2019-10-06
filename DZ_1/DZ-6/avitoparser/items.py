# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

def empty(values):
    if values is not None and values != ' ':
        return values

class AvitoRealEstate(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    model = scrapy.Field(output_processor=MapCompose(empty))
    year = scrapy.Field(output_processor=MapCompose(empty))
    price = scrapy.Field(output_processor=TakeFirst())



