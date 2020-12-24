# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
import scrapy

class PptPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['download_url'],meta={'parent_name':item['parent_name'],'ppt_name':item['ppt_file_name']})

    def file_path(self, request, response=None, info=None):
        parent_name=request.meta['parent_name']
        ppt_name=request.meta['ppt_name']
        filename='{}/{}.zip'.format(parent_name,ppt_name)
        return filename
