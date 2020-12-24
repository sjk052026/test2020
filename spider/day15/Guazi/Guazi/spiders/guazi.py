# -*- coding: utf-8 -*-
import scrapy
from ..items import GuaziItem


class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['www.guazi.com']
    start_urls = ['https://www.guazi.com/sh/buy/o1/#bread']

    def parse(self, response):
        li_list = response.xpath('//ul[@class="carlist clearfix js-top"]/li')
        for li in li_list:
            # /a[1]/@title
            # /a[1]/@href
            # /a/div[2]/p/text()
            item = GuaziItem()
            item['name'] = li.xpath('./a[1]/@title').get()
            item['link'] = li.xpath('./a[1]/@href').get()
            item['price'] = li.xpath('./a/div[2]/p/text()').get()
            yield item

