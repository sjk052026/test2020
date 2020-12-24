# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 文件管道用法
from scrapy.pipelines.files import FilesPipeline
import scrapy

class PptPipeline(FilesPipeline):
    # 重写get_media_requests()方法
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['download_url'], meta={'parent_name':item['parent_name'], 'ppt_name':item['ppt_file_name']})

    # 处理文件名: 重写file_path()方法
    def file_path(self, request, response=None, info=None):
        # filename: 校园风格PPT/新学期家长会PPT模板.zip
        parent_name = request.meta['parent_name']
        ppt_name = request.meta['ppt_name']
        filename = '{}/{}.zip'.format(parent_name, ppt_name)
        print(filename)

        return filename





