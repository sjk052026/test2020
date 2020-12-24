# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 定义要抓取的数据结构
class GuaziItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
