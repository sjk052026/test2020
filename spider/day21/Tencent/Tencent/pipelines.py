# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class TencentPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item


import pymysql
from .settings import *


class TencentMysqlPipeline:
    def open_spider(self, spider):
        self.db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB, charset=CHARSET)
        self.cur = self.db.cursor()
        self.ins = 'insert into tencenttab values(%s,%s,%s,%s,%s,%s)'

    def process_item(self, item, spider):
        li = [
            item['job_name'],
            item['job_type'],
            item['job_duty'],
            item['job_require'],
            item['job_add'],
            item['job_time']
        ]
        self.cur.execute(self.ins, li)
        self.db.commit()
        return item

    def close_spider(self, spider):
        self.db.close()
        self.cur.close()
