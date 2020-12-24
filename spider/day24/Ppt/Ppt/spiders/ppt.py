# -*- coding: utf-8 -*-
import scrapy
from ..items import PptItem


class PptSpider(scrapy.Spider):
    name = 'ppt'
    allowed_domains = ['www.1ppt.com']
    start_urls = ['http://www.1ppt.com/xiazai/']

    def parse(self, response):
        """一级页面解析函数: 提取 栏目分类名称、分类链接"""
        li_list = response.xpath('//div[@class="col_nav clearfix"]/ul/li')
        # li_list[1:] : 因为第一个元素是：栏目分类
        for li in li_list[1:]:
            item = PptItem()
            item['parent_name'] = li.xpath('./a/text()').get()
            parent_url = 'http://www.1ppt.com' + li.xpath('./a/@href').get()
            # 将parent_url交给调度器入队列
            yield scrapy.Request(
                url=parent_url,
                meta={'meta0': item, 'parent_url': parent_url},
                callback=self.get_total_page
            )

    def get_total_page(self, response):
        meta0 = response.meta['meta0']
        parent_url = response.meta['parent_url']
        # last_href:ppt_zongjie_22.html
        last_href = response.xpath('//ul[@class="pages"]/li[last()]/a/@href').get()
        if last_href:
            total_page = int(last_href.split('.')[0].split('_')[-1])
            for page in range(1, total_page + 1):
                page_url = parent_url + 'ppt_{}_{}.html'.format(last_href.split('_')[-2], page)
                yield scrapy.Request(url=page_url, meta={'meta1': meta0}, callback=self.parse_two_page)
        else:
            yield scrapy.Request(url=parent_url, meta={'meta1': meta0}, callback=self.parse_two_page, dont_filter=True)

    def parse_two_page(self, response):
        """二级页面解析函数: 提取 PPT名字、PPT链接、总页数"""
        meta1 = response.meta['meta1']
        li_list = response.xpath('//ul[@class="tplist"]/li')
        for li in li_list:
            # 只要有继续交往调度器的请求,则必须创建新的item对象
            item = PptItem()
            item['ppt_file_name'] = li.xpath('./h2/a/text()').get()
            item['parent_name'] = meta1['parent_name']
            ppt_url = 'http://www.1ppt.com' + li.xpath('./h2/a/@href').get()

            # 交给调度器入队列
            yield scrapy.Request(
                url=ppt_url,
                meta={'meta2': item},
                callback=self.parse_three_page
            )

    def parse_three_page(self, response):
        """三级页面解析函数: 提取进入PPT下载页的链接"""
        item = response.meta['meta2']
        # 进入ppt下载页的链接
        ppt_page_url = 'http://www.1ppt.com' + response.xpath('//ul[@class="downurllist"]/li/a/@href').get()
        # 交给调度器入队列
        yield scrapy.Request(
            url=ppt_page_url,
            meta={'item': item},
            callback=self.parse_four_page
        )

    def parse_four_page(self, response):
        """四级页面解析函数: 提取真正PPT下载链接"""
        item = response.meta['item']
        item['download_url'] = response.xpath('//ul[@class="downloadlist"]/li[1]/a/@href').get()

        # 至此,一条完整的数据提取完成,交给项目管道处理
        yield item
