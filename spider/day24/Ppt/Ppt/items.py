# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PptItem(scrapy.Item):
    # 定义哪些要抓取的数据结构？考虑pipelines.py中需要什么？
    # filename: ./ppt/工作总结PPT/xxxx.zip
    # PPT下载链接、PPT模板名字、栏目分类名字
    download_url = scrapy.Field()
    ppt_file_name = scrapy.Field()
    parent_name = scrapy.Field()








