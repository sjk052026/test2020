# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PptItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    download_url = scrapy.Field()
    ppt_file_name = scrapy.Field()
    parent_name = scrapy.Field()
