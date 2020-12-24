# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class DaomubijiPipeline(object):
    def process_item(self, item, spider):
        filename='{}{}.txt'.format(
            item['directory'],
            item['son_title'].replace(' ','_')
        )
        with open(filename,'w') as f:
            f.write(item['content'])

        return item
