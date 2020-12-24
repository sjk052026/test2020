# -*- coding: utf-8 -*-
import scrapy
import os
from ..items import DaomubijiItem


class DaomuSpider(scrapy.Spider):
    name = 'daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    def parse(self, response):
        """一级页面的解析函数:提取大标题和大链接"""
        a_list = response.xpath('//li[contains(@id,"menu-item-20")]/a')
        for a in a_list:
            parent_title = a.xpath('./text()').get()
            parent_url = a.xpath('./@href').get()
            # ./ novel / 盗墓笔记1: 七星鲁王宫/
            item = DaomubijiItem()
            item['directory'] = './novel/{}/'.format(parent_title)
            if not os.path.exists(item['directory']):
                os.makedirs(item['directory'])
            yield scrapy.Request(url=parent_url, meta={'meta1': item}, callback=self.detail_page)

    def detail_page(self, response):
        meta1_item = response.meta['meta1']
        article_list = response.xpath('//article')
        for article in article_list:
            item=DaomubijiItem()
            son_url = article.xpath('./a/@href').get()
            item['son_title']=article.xpath('./a/text()').get()
            item['directory']=meta1_item['directory']
            yield scrapy.Request(url=son_url, meta={'item': item}, callback=self.get_content)

    def get_content(self, response):
        item = response.meta['item']
        p_list = response.xpath('//article[@class="article-content"]/p/text()').extract()
        print(p_list)
        item['content'] = '\n'.join(p_list)
        print(item['content'])
        yield item
