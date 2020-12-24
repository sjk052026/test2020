import re
from hashlib import md5

import requests
import redis
import pymysql
import random
import time
import sys


class MoveSpider:
    def __init__(self):
        self.url = 'http://www.4567kan.com/index.php/vod/show/id/5/page/{}.html'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
        self.db = pymysql.connect('localhost', 'root', '123456', 'movedb', charset='utf8')
        self.cur = self.db.cursor()
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers).content.decode('utf-8')
        return html

    def re_func(self, regex, html):
        pattern = re.compile(regex, re.S)
        r_list = pattern.findall(html)
        return r_list

    def md5_href(self, href):
        s = md5()
        s.update(href.encode())
        return s.hexdigest()

    def parse_html(self, one_url):
        one_html = self.get_html(one_url)
        one_regex = '<div class="stui-vodlist__box">.*?href="(.*?)"'
        href_list=self.re_func(one_regex,one_html)
        for href in href_list:
            finger=self.md5_href(href)
            if self.r.sadd('move:spiders',finger)==1:
                self.get_move_info(href)
                time.sleep(random.randint(1,2))
            else:
                sys.exit('更新完成')

    def get_move_info(self,href):
        two_url='http://www.4567kan.com'+href
        two_html=self.get_html(url=two_url)
        two_regex='<div class="stui-content__detail">.*?<h1 class="title">(.*?)</h1>.*?<span class="detail-sketch">(.*?)</span>'
        move_info_list=self.re_func(two_regex,two_html)
        ins='insert into movetab values(%s,%s)'
        li=[
            move_info_list[0][0].strip(),
            move_info_list[0][1].strip(),
        ]
        self.cur.execute(ins,li)
        self.db.commit()
        print(li)

    def run(self):
        for page in range(1,6):
            page_url=self.url.format(page)
            self.parse_html(one_url=page_url)
        self.cur.close()
        self.db.close()

if __name__ == '__main__':
    spider=MoveSpider()
    spider.run()

"""
use movedb;
create table movetab(
name varchar(100),
intro varchar(2000)
)charset=utf8;
"""