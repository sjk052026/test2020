# -*- coding: utf-8 -*-
import scrapy
from ..items import PptItem


class PptSpider(scrapy.Spider):
    name = 'ppt'
    allowed_domains = ['www.1ppt.com']
    start_urls = ['http://www.1ppt.com/xiazai/']

    def parse(self, response):
        print(response.text)
        li_list = response.xpath('//div[@class="col_nav clearfix"]/ul/li')
        for li in li_list[1:]:
            item = PptItem()
            item['parent_name'] = li.xpath('./a/text()').get()
            print(item['parent_name'])
            parent_url = 'http://www.1ppt.com' + li.xpath('./a/@href').get()
            yield scrapy.Request(url=parent_url, meta={'meta1': item}, callback=self.parse_two_page)

    def parse_two_page(self, response):
        meta1 = response.meta['meta1']
        li_list = response.xpath('//ul[@class="tplist"]/li')
        for li in li_list:
            item = PptItem()
            item['ppt_file_name'] = li.xpath('./h2/a/text()').get()
            item['parent_name'] = meta1['parent_name']
            ppt_url = 'http://www.1ppt.com' + li.xpath('./h2/a/@href').get()
            yield scrapy.Request(url=ppt_url, meta={'meta2': item}, callback=self.parse_three_page)

    def parse_three_page(self, response):
        item = response.meta['meta2']
        ppt_page_url = 'http://www.1ppt.com' + response.xpath('//ul[@class="downurllist"]/li/a/@href').get()
        yield scrapy.Request(url=ppt_page_url, meta={'item': item}, callback=self.parse_four_page)

    def parse_four_page(self, response):
        item = response.meta['item']
        item['download_url'] = response.xpath('//ul[@class="downloadlist"]/li[1]/a/@href').get()
        yield item
