# -*- coding: utf-8 -*-
import scrapy
import requests
import json
from ..items import KfcItem
from lxml import etree


class KfcSpider(scrapy.Spider):
    name = 'kfc'
    allowed_domains = ['www.kfc.com.cn']
    post_url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'

    def get_total_page(self,city):
        formdata = {
            'cname': city,
            'pid': '',
            'pageIndex': '1',
            'pageSize': '10',
        }
        headers = {'User-Agent': 'Mozilla/5.0'}
        html = requests.post(url=self.post_url, data=formdata, headers=headers).json()
        count = html['Table'][0]['rowcount']
        total_page = count // 10 if count % 10 == 0 else count // 10 + 1
        return total_page

    def get_all_city_li(self):
        city_url='http://www.kfc.com.cn/kfccda/storelist/index.aspx'
        headers={'User-Agent':'Mozilla/5.0'}
        city_html=requests.get(url=city_url,headers=headers).text
        p=etree.HTML(city_html)
        all_city_li=p.xpath('//ul[@class="shen_info"]/li/div/a/text()')
        return all_city_li

    def start_requests(self):
        all_city_li=self.get_all_city_li()
        for city in all_city_li:
            total_page = self.get_total_page(city)
            for page_index in range(1, total_page + 1):
                formdata = {
                    'cname': city,
                    'pid': '',
                    'pageIndex': str(page_index),
                    'pageSize': '10',
                }
                yield scrapy.FormRequest(url=self.post_url, formdata=formdata, callback=self.get_shop_info)

    def get_shop_info(self, response):
        #text属性:获取响应内容-字符串
        #json.loads():把json格式的字符串转为python数据类型
        html=json.loads(response.text)
        for one_shop_dict in html['Table1']:
            item=KfcItem()
            item['number']=one_shop_dict['rownum']
            item['name']=one_shop_dict['storeName']
            item['address']=one_shop_dict['addressDetail']
            item['city']=one_shop_dict['cityName']
            yield item
