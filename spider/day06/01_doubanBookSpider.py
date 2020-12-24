"""
豆瓣图书top250
"""
import requests
from lxml import etree
import time
import random
from fake_useragent import UserAgent


class DoubanSpider:
    def __init__(self):
        self.url = 'https://book.douban.com/top250?start={}'

    def get_html(self, url):
        # useragent池建立在这里
        headers = {'User-Agent': UserAgent().random}
        html = requests.get(url=url, headers=headers).content.decode('utf-8', 'ignore')
        # 直接调用解析函数
        self.parse_html(html)

    def parse_html(self, html):
        """xpath解析提取数据"""
        p = etree.HTML(html)
        # 基准xpath:节点对象列表
        table_list = p.xpath('//div[@class="indent"]/table')
        for table in table_list:
            item={}
            name_list=table.xpath('.//div[@class="pl2"]/a/@title')
            item['name']=name_list[0].strip() if name_list else None
            info_list=table.xpath('.//p[@class="pl"]/text()')
            item['info']=info_list[0].strip().split('/') if info_list else None
            score_list=table.xpath('.//span[@class="rating_nums"]/text()')
            item['score']=score_list[0].strip() if score_list else None
            commit_list=table.xpath('.//span[@class="pl"]/text()')
            item['commit']=commit_list[0].strip()[1:-1].strip() if commit_list else None
            comment_list=table.xpath('.//span[@class="inq"]/text()')
            item['comment']=comment_list[0].strip() if comment_list else None

            print(item)

    def run(self):
        for page in range(1,11):
            start=(page-1)*25
            page_url=self.url.format(start)
            self.get_html(url=page_url)
            time.sleep(random.randint(1,2))

if __name__ == '__main__':
    spider=DoubanSpider()
    spider.run()