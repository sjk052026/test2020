import requests
import re
import time
import random
import pymysql


class CarSpider:
    def __init__(self):
        self.url = 'https://www.che168.com/beijing/a0_0msdgscncgpi1lto1csp{}exx0/?pvareaid=102179#currengpostion'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers).text
        self.parse_html(html)

    def parse_html(self, html):
        regex = '<div class="cards-bottom">.*?<h4 class="card-name">(.*?)</h4>.*?<p class="cards-unit">(.*?)</p>.*?<span class="pirce"><em>(.*?)</em>'
        pattern = re.compile(regex, re.S)
        car_list = pattern.findall(html)
        self.save_html(car_list)

    def save_html(self, car_list):
        for car in car_list:
            item = {}
            item['car_name'] = car[0].strip()
            item['car_info'] = car[1].strip()
            item['car_price'] = car[2].strip()
            print(item)

    def run(self):
        for page in range(1, 6):
            page_url = self.url.format(page)
            self.get_html(url=page_url)
            time.sleep(random.randint(1,2))

if __name__ == '__main__':
    spider=CarSpider()
    spider.run()
