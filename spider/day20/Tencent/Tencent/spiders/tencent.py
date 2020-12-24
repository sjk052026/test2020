# -*- coding: utf-8 -*-
import scrapy


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    start_urls = ['http://careers.tencent.com/']

    def parse(self, response):
        pass
