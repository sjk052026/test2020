"""
抓取民政部网站最新月份行政区划代码
思路:
1.一级页面:提取最新月份的链接
2.二级页面:提取具体数据
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
import re
import redis
from hashlib import md5
import sys


class MzbSpider:
    def __init__(self):
        self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2020/'
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def get_html(self, url):
        self.headers = {'User_Agent': UserAgent().random}
        html = requests.get(url=url, headers=self.headers).content.decode('utf-8', 'ignore')

        return html

    def xpath_func(self, html, x):
        p = etree.HTML(html)
        r_list = p.xpath(x)

        return r_list

    def md5_href(self, href):
        s = md5()
        s.update(href.encode())

        return s.hexdigest()

    def parse_html(self):
        """爬虫逻辑函数"""
        one_html = self.get_html(url=self.url)
        one_x = '//table/tr[1]/td[@class="arlisttd"]/a/@href'
        # 此处注意:响应内容中没有tbody节点
        href_list = self.xpath_func(one_html, one_x)
        # print(href_list)
        # href:最新月份的链接
        href = href_list[0].strip()
        finger = self.md5_href(href)
        if self.r.sadd('mzb:spider', finger) == 1:
            # 向href发请求提取具体数据
            self.get_data(href)
        else:
            sys.exit('更新完成')

    def get_data(self, href):
        """二级页面解析提取真实返回数据"""
        two_url = 'http://www.mca.gov.cn' + href
        two_html = self.get_html(url=two_url)
        # two_html中有JS进行了URL地址的跳转
        # 从two_html中提取真实返回数据的链接
        regex = 'window.location.href="(.*?)"'
        pattern = re.compile(regex, re.S)
        really_href = pattern.findall(two_html)[0].strip()
        # 提取具体数据的函数
        self.parse_two_page(really_href)

    def parse_two_page(self, really_href):
        """提取真实数据的函数"""
        really_html = self.get_html(url=really_href)
        two_x = '//tr[@height="19"]'
        tr_list = self.xpath_func(really_html, two_x)
        print(tr_list)
        for tr in tr_list:
            item = {}
            item['name'] = tr.xpath('./td[3]/text()')[0].strip()
            item['code'] = tr.xpath('./td[2]/text() | ./td[2]/span/text()')[0].strip()
            print(item)

    def run(self):
        self.parse_html()


if __name__ == '__main__':
    spider = MzbSpider()
    spider.run()
