# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import SoItem


class SoSpider(scrapy.Spider):
    name = 'so'
    allowed_domains = ['image.so.com']

    def start_requests(self):
        for i in range(5):
            page_url = 'https://image.so.com/zjl?ch=beauty&sn={}&listtype=new&temp=1'.format(i * 30)
            yield scrapy.Request(url=page_url, callback=self.get_image_url)

    def get_image_url(self, response):
        html = json.loads(response.text)
        for one_image_dict in html['list']:
            item = SoItem()
            item['image_url'] = one_image_dict['qhimg_url']
            item['image_title']=one_image_dict['title']
            yield item