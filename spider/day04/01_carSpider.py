import requests
import re
import time
import random
import pymysql


class CarSpider:
    def __init__(self):
        self.url = 'https://www.che168.com/shanghai/a0_0msdgscncgpi1lto1csp{}exx0/?pvareaid=102179#currengpostion'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201'}
        self.db = pymysql.connect('localhost', 'root', '123456', 'cardb', charset='utf8')
        self.cur = self.db.cursor()

    def get_html(self, url):
        """功能函数1:发请求获取响应内容"""
        html = requests.get(url=url, headers=self.headers).text

        return html

    def re_func(self, regex, html):
        """功能函数2:正则解析功能函数"""
        pattern = re.compile(regex, re.S)
        r_list = pattern.findall(html)

        return r_list

    def parse_html(self, one_url):
        """爬虫逻辑从此处开始"""
        # one_html:一级页面的响应内容
        one_html = self.get_html(url=one_url)
        one_regex = '<li class="cards-li list-photo-li".*?<a href="(.*?)"'
        href_list = self.re_func(one_regex, one_html)
        for href in href_list:
            # get_car_info:抓取一辆汽车的详细数据
            self.get_car_info(href)
            time.sleep(random.randint(1, 2))

    def get_car_info(self, href):
        """提取一辆汽车具体数据的函数"""
        two_url = 'https://www.che168.com/' + href
        two_html = self.get_html(url=two_url)
        two_regex = '<div class="car-box">.*?<h3 class="car-brand-name">(.*?)</h3>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<span class="price" id="overlayPrice">￥(.*?)<b>'
        car_info_list = self.re_func(two_regex, two_html)
        self.save_html(car_info_list)

    def save_html(self, car_info_list):
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
            self.parse_html(page_url)
        self.cur.close()
        self.db.close()


if __name__ == '__main__':
    spider = CarSpider()
    spider.run()
