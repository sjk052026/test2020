import requests
from lxml import etree
from fake_useragent import UserAgent
import redis
from hashlib import md5
import re


class MzbSpider:
    def __init__(self):
        self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2020/'
        self.headers = {'User-Agent': UserAgent().random}
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def get_html(self, url):
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
        one_html = self.get_html(self.url)
        one_x = '//table/tr[1]/td[@class="arlisttd"]/a/@href'
        href_list = self.xpath_func(one_html, one_x)
        href = href_list[0].strip()
        two_url = 'http://www.mca.gov.cn' + href

        finger = self.md5_href(two_url)
        if self.r.sadd('mzb:spider', finger) == 1:
            self.parse_two_html(two_url=two_url)
        else:
            print("数据已更新")

    def parse_two_html(self, two_url):
        two_html = self.get_html(url=two_url)
        regex = 'window.location.href="(.*?)"'
        pattern = re.compile(regex, re.S)
        real_href = pattern.findall(two_html)[0].strip()
        self.parse_real_data(real_href)

    def parse_real_data(self, real_href):
        real_html = self.get_html(real_href)
        two_x = '//tr[@height="19"]'
        tr_list = self.xpath_func(real_html, two_x)
        for tr in tr_list:
            item = {}
            item["city"] = tr.xpath('./td[3]/text()')[0].strip()
            item["code"] = tr.xpath('./td[2]/text() | ./td[2]/span/text()')[0].strip()
            print(item)

    def run(self):
        self.parse_html()


if __name__ == '__main__':
    spider = MzbSpider()
    spider.run()
