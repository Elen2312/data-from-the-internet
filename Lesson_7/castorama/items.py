# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst


def process_goods(goods):
    goods = " ".join(str(goods).split()).replace('\\n', '')
    return goods


def process_price(price):
    price = int(price[0].replace(' ', ''))
    return price


def process_photo(photo):
    photo = 'https://www.castorama.ru' + photo
    return photo


class CastoramaItem(scrapy.Item):
    # define the fields for your item here like:
    goods = scrapy.Field(input_processor=Compose(process_goods), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field(input_processor=MapCompose(process_photo))
