# -*- coding: utf-8 -*-
import scrapy


class DaomubijiSpider(scrapy.Spider):
    name = 'daomubiji'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    def parse(self, response):
        pass
