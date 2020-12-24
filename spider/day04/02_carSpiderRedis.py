"""
Redis中集合实现增量爬虫
思路:
    1.将每一个汽车详情页的URL地址生成指纹,存到redis集合中
    2.利用sadd()方法的返回值来确定之前是否抓取过
      返回值为1: 没抓过！！说明添加成功,说明集合中之前没有这个指纹
      返回值为0: 之前抓过！！说明没添加成功,说明集合中之前已经存在这个指纹
"""
import requests
import re
import time
import random
import pymysql
# 对url地址进行md5的加密,生成请求指纹,最终存放到redis的集合中
from hashlib import md5
import redis
import sys


class CarSpider:
    def __init__(self):
        """定义常用变量"""
        self.url = 'https://www.che168.com/langfang/a0_0msdgscncgpi1lto1csp{}exx0/?pvareaid=102179#currengpostion'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
        # 创建2个对象 - mysql - 为了存储数据
        self.db = pymysql.connect('localhost', 'root', '123456', 'cardb', charset='utf8')
        self.cur = self.db.cursor()
        # 连接redis - 为了实现增量爬虫
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def get_html(self, url):
        """功能函数1:发请求获取响应内容"""
        html = requests.get(url=url, headers=self.headers).text

        return html

    def re_func(self, regex, html):
        """功能函数2:正则解析功能函数"""
        pattern = re.compile(regex, re.S)
        r_list = pattern.findall(html)

        return r_list

    def md5_href(self, href):
        """功能函数3:对href进行md5的加密"""
        s = md5()
        s.update(href.encode())

        return s.hexdigest()

    def parse_html(self, one_url):
        """爬虫逻辑从此处开始"""
        # one_html: 一级页面响应内容
        one_html = self.get_html(url=one_url)
        one_regex = '<li class="cards-li list-photo-li".*?<a href="(.*?)"'
        # href_list: ['/dealer/xxx','/dealer/xxx','',...,'']
        href_list = self.re_func(one_regex, one_html)
        for href in href_list:
            # 生成指纹
            finger = self.md5_href(href)
            # 返回值为1: 说明没抓过(因为集合中之前没有)
            if self.r.sadd('car:spiders', finger) == 1:
                # get_car_info: 抓取一辆汽车的详细数据
                self.get_car_info(href)
                time.sleep(random.randint(1, 2))
            else:
                # 彻底终止这个程序!!!
                sys.exit('更新完成')

    def get_car_info(self, href):
        """提取一辆汽车具体数据的函数"""
        two_url = 'https://www.che168.com' + href
        two_html = self.get_html(url=two_url)
        two_regex = '<div class="car-box">.*?<h3 class="car-brand-name">(.*?)</h3>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<span class="price" id="overlayPrice">￥(.*?)<b>'
        car_info_list = self.re_func(two_regex, two_html)
        # car_info_list:
        # [('五菱之光', '3.8万公里', '2008年01月', '手动 / 1L', '廊坊', '0.30')]
        ins = 'insert into cartab values(%s,%s,%s,%s,%s,%s,%s)'
        li = [
            car_info_list[0][0].strip(),
            car_info_list[0][1].strip(),
            car_info_list[0][2].strip(),
            car_info_list[0][3].split('/')[0].strip(),
            car_info_list[0][3].split('/')[1].strip(),
            car_info_list[0][4].strip(),
            car_info_list[0][5].strip(),
        ]
        self.cur.execute(ins, li)
        self.db.commit()
        print(li)

    def run(self):
        """程序入口函数"""
        for page in range(1, 3):
            page_url = self.url.format(page)
            self.parse_html(one_url=page_url)
        # 所有数据抓取完成后,关闭游标,断开数据库连接
        self.cur.close()
        self.db.close()


if __name__ == '__main__':
    spider = CarSpider()
    spider.run()
