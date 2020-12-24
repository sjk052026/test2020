"""
抓取豆瓣电影排行榜中所有类别的所有电影
"""
import requests
import json
import time
import random
import re


class DoubanSpider:
    def __init__(self):
        # url: F12抓包抓到的返回json数据的地址
        self.url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    def get_html(self, url):
        """功能函数: 发请求获取响应内容"""
        html = requests.get(url=url, headers=self.headers).text

        return html

    def parse_html(self, url):
        """爬虫逻辑函数由此开始:提取具体电影数据"""
        html = self.get_html(url=url)
        # json.loads():把json格式的字符串转为python数据类型
        # html: [{}, {}, {}, {}, ...]
        html = json.loads(html)
        for one_film_dict in html:
            item = {}
            item['rank'] = one_film_dict['rank']
            item['name'] = one_film_dict['title']
            item['score'] = one_film_dict['score']
            item['time'] = one_film_dict['release_date']
            print(item)

    def get_total(self, typ):
        """获取某个类别下电影的总数"""
        total_url = 'https://movie.douban.com/j/chart/top_list_count?type={}&interval_id=100%3A90'.format(typ)
        html = json.loads(self.get_html(url=total_url))

        return html['total']

    def get_all_type_dict(self):
        """获取所有类别的大字典"""
        url = 'https://movie.douban.com/chart'
        html = self.get_html(url=url)
        regex = '<span><a href=".*?type_name=(.*?)&type=(.*?)&interval_id=100:90&action=">'
        pattern = re.compile(regex, re.S)
        # r_list:[('剧情','11'),('喜剧','24'),...,()]
        r_list = pattern.findall(html)
        # 把r_list处理成字典
        all_type_dict = {}
        for r in r_list:
            all_type_dict[r[0]] = r[1]

        return all_type_dict

    def run(self):
        """程序入口函数"""
        # {'剧情':'24','喜剧':'11', '爱情':'13'...}
        all_type_dict = self.get_all_type_dict()
        # 终端给出所有电影的提示
        menu = ''
        for d in all_type_dict:
            menu = menu + d + '|'
        print(menu)

        t = input('请输入电影类别:')
        typ = all_type_dict[t]
        # 获取typ类别的电影总数
        total = self.get_total(typ)
        for start in range(0, total, 20):
            page_url = self.url.format(typ, start)
            self.parse_html(url=page_url)
            # 控制频率
            time.sleep(random.randint(1, 2))


if __name__ == '__main__':
    spider = DoubanSpider()
    spider.run()
