# -*- coding: utf-8 -*-
import scrapy


class BaixiaoduSpider(scrapy.Spider):
    name = 'baixiaodu'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        print(response.xpath('//title/text()'))
        print(response.xpath('//title/text()').extract())
        print(response.xpath('//title/text()').extract_first())
        res=response.xpath('//title/text()').get()
        print(res,type(res))

        #text属性:获取响应的内容-字符串
        print(response.text)
        #body属性:获取响应的内容-字节串
        print(response.body)