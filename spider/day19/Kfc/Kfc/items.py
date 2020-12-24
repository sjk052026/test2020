# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KfcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 门店编号 门店名称 门店地址 所属城市
    number=scrapy.Field()
    name=scrapy.Field()
    address=scrapy.Field()
    city=scrapy.Field()
