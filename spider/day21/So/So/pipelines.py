# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class SoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['image_url'], meta={'title': item['image_title']})

    def file_path(self, request, response=None, info=None):
        title = request.meta['title']
        filename = title + '.jpg'
        return filename
